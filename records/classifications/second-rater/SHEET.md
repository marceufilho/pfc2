# Second rater's sheet: does the contract restate the function body?

**Do not open `KEY.json`** (next to this file) and do not open
`docs/evaluation/reports/PHASE-4-contract-restatement.json` or the units' `notes.json` before you have finished.
They hold another reader's label for every unit below. Your answers are yours alone: nobody else fills them in.

**Allowed answers**, written in `ANSWERS.json` in place of each `null`, quotes included:

- `"restates"`: the contract restates the body;
- `"different"`: the contract states a property in different terms;
- `"unclear"`: you cannot decide.

This sheet lists 32 small C functions, each with a contract: `requires(...)` is what the caller must
guarantee, `ensures(...)` is what the function guarantees about `result` (its return value) or about the array it
writes. A verifier proved every one of these contracts; that is not in question. For each unit you see the function
with its contract (comments removed) and, below it, the requirement as the upstream benchmark states it. The order
was drawn with seed 20261123 by `tools/author_review.py second-rater-sheet`.

## The rule

One question per unit, about the `ensures` clauses only (ignore `requires` and loop `invariant`s):

- **restates**: the `ensures` is the same expression, or the same case analysis, as the code of the body, possibly
  with trivial rewriting (an `if` written as an implication, operands reordered). Someone could have produced it
  by copying the body into the contract.
- **different**: the `ensures` describes the result in terms other than the ones the body computes with: a bound,
  a relation between inputs and result, an inverse operation, "the result is one of the inputs". A body of the same
  shape with a mistake in it would not satisfy the contract by construction. If some clauses repeat the body and at
  least one other says something about the result in different terms, answer **different**.
- **unclear**: you cannot decide between the two.

Judge what is written, not whether a better contract could exist, and not whether the upstream requirement is
itself a formula.

Two worked examples (neither is one of the 32 units):

*Example 1: restates.* The contract is the returned expression.

```c
long perimeter(long w, long h)
    requires(0 <= w && w <= 1000 && 0 <= h && h <= 1000)
    ensures(result == 2 * (w + h))
{
    return 2 * (w + h);
}
```

*Example 2: different.* The body counts upwards in a loop; the contract never mentions the loop and instead bounds
the result from both sides (`result` is the largest number whose double does not exceed `n`).

```c
long half(long n)
    requires(n >= 0)
    ensures(2 * result <= n && n < 2 * result + 2)
{
    long q = 0;
    while (2 * (q + 1) <= n)
        invariant(0 <= q && 2 * q <= n)
    {
        q = q + 1;
    }
    return q;
}
```

## What to do

1. Under each unit tick a box if you like (the boxes and the `Notes:` lines are for you), and write your answer
   in `ANSWERS.json`, replacing `null` with one of the three strings above.
2. When no `null` is left, return `ANSWERS.json`, or run
   `uv run --locked python tools/author_review.py second-rater-score` from the repository root. It refuses an
   unfinished form, never changes `ANSWERS.json`, and writes `SCORE.json`.

---

## U01

The function with its contract, comments removed:

```c
#include "pfc.h"
long lastDigit(long n)
    requires(n >= 0)
    ensures(0 <= result && result < 10)
    ensures(result == n % 10)
{
    return n % 10;
}
```

Verina's description:

```
-----Description-----  
This task requires writing a Lean 4 method that extracts the last digit of a given non-negative integer. The method should return the last digit, which is obtained by computing the remainder when the number is divided by 10. The result must always be between 0 and 9.

-----Input-----  
The input consists of a single value:  
n: A non-negative integer.

-----Output-----  
The output is an integer:  
Returns the last digit of the input number, ensuring that the digit lies within the range 0 to 9.

-----Note-----  
It is assumed that the input number n is non-negative.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (0 ≤ result ∧ result < 10) ∧
  (n % 10 - result = 0 ∧ result - n % 10 = 0)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U02

The function with its contract, comments removed:

```c
#include "pfc.h"
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    long twice = 2 * x;
    return twice + x;
}
```

Verina's description:

```
-----Description-----  
This problem involves computing the triple of a given integer. The goal is to produce an output that is exactly three times the input value.

-----Input-----  
The input consists of:  
• x: An integer representing the value to be tripled.

-----Output-----  
The output is an integer that is three times the input value (i.e., 3 * x).

-----Note-----  
The implementation uses a local variable to first compute double the input and then adds the original input to get the final result. The accompanying theorem asserts that the function satisfies the specification of computing 3 * x.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result / 3 = x ∧ result / 3 * 3 = result
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U03

The function with its contract, comments removed:

```c
#include "pfc.h"
long Swap(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == Y && out[1] == X)
    ensures(X == Y || (out[0] != X && out[1] != Y))
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
```

Verina's description:

```
-----Description-----  
This task involves creating a function that swaps two integer values. Given two integers, the function should return a pair where the first element is the second input value and the second element is the first input value.

-----Input-----  
The input consists of two integers:  
• X: An integer representing the first value.  
• Y: An integer representing the second value.

-----Output-----  
The output is a pair (Int × Int) that:  
• Contains the original Y as the first element.  
• Contains the original X as the second element.

-----Note-----  
There are no additional preconditions. The function simply swaps the two input values.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result.fst = Y ∧ result.snd = X ∧
  (X ≠ Y → result.fst ≠ X ∧ result.snd ≠ Y)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U04

The function with its contract, comments removed:

```c
#include "pfc.h"
long SwapSimultaneous(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == Y && out[1] == X)
    ensures(X == Y || (out[0] != X && out[1] != Y))
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
```

Verina's description:

```
-----Description-----  
This task requires swapping two integer values. Given two integers as input, the objective is to produce an output where their order is reversed: the first element of the output corresponds to the second input and the second element corresponds to the first input.

-----Input-----  
The input consists of two integers:  
• X: An integer value.  
• Y: Another integer value.

-----Output-----  
The output is a tuple (Int × Int) where:  
• The first element is equal to Y.  
• The second element is equal to X.

-----Note-----  
There are no additional preconditions for this task. The function simply returns a swapped tuple of its two input integers.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result.1 = Y ∧ result.2 = X ∧
  (X ≠ Y → result.fst ≠ X ∧ result.snd ≠ Y)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U05

The function with its contract, comments removed:

```c
#include "pfc.h"
long minOfThree(long a, long b, long c)
    ensures(result <= a && result <= b && result <= c)
    ensures(result == a || result == b || result == c)
{
    long min = a;
    if (b < min) {
        min = b;
    }
    if (c < min) {
        min = c;
    }
    return min;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that finds the minimum among three given integers. The method should return the smallest value, ensuring that the result is less than or equal to each of the input numbers and that it is one of the provided integers.

-----Input-----
The input consists of three integers:
a: The first integer.
b: The second integer.
c: The third integer.

-----Output-----
The output is an integer:
Returns the minimum of the three input numbers, assuring that the returned value is less than or equal to a, b, and c, and that it matches one of these values.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (result <= a ∧ result <= b ∧ result <= c) ∧
  (result = a ∨ result = b ∨ result = c)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U06

The function with its contract, comments removed:

```c
#include "pfc.h"
long DivisionFunction(long x, long y, long out_cap, long out[out_cap])
    requires(x >= 0)
    requires(y >= 0)
    requires(out_cap >= 2)
    ensures(y != 0 || (out[0] == x && out[1] == 0))
    ensures(y == 0 || (out[1] * y + out[0] == x && 0 <= out[0] && out[0] < y && 0 <= out[1]))
{
    if (y == 0) {
        out[0] = x;
        out[1] = 0;
        return 0;
    }
    out[0] = x % y;
    out[1] = x / y;
    return 0;
}
```

Verina's description:

```
-----Description-----  
This task involves performing integer division with remainder on natural numbers. Given two natural numbers, x (the dividend) and y (the divisor), the objective is to determine the quotient and remainder. When y is non-zero, the quotient and remainder should satisfy the condition that the dividend equals the divisor multiplied by the quotient plus the remainder, with the remainder being nonnegative and strictly less than y. In the case where y is zero, the result should indicate that no division is performed by returning x as the quotient and 0 as the remainder.

-----Input-----  
The input consists of two natural numbers:  
• x: A natural number representing the dividend.  
• y: A natural number representing the divisor.

-----Output-----  
The output is a pair of integers (r, q) where:  
• If y ≠ 0, then q is the quotient and r is the remainder such that:  
   - q * Int.ofNat y + r = Int.ofNat x  
   - 0 ≤ r < Int.ofNat y  
   - 0 ≤ q  
• If y = 0, then the output is (Int.ofNat x, 0).

-----Note-----  
The specification regarding the division properties applies only when y is non-zero. When y = 0, the function safely returns (x, 0) in its integer form.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  let (r, q) := result;
  (y = 0 → r = Int.ofNat x ∧ q = 0) ∧
  (y ≠ 0 → (q * Int.ofNat y + r = Int.ofNat x) ∧ (0 ≤ r ∧ r < Int.ofNat y) ∧ (0 ≤ q))
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U07

The function with its contract, comments removed:

```c
#include "pfc.h"
long maxOfThree(long a, long b, long c)
    ensures(result >= a && result >= b && result >= c)
    ensures(result == a || result == b || result == c)
{
    long best = a;
    if (b > best) {
        best = b;
    }
    if (c > best) {
        best = c;
    }
    return best;
}
```

Verina's description:

```
-----Description-----
This task requires writing a Lean 4 method that finds the maximum among three given integers. The method should return the largest value, ensuring that the result is greater than or equal to each of the input numbers and that it is one of the provided integers.

-----Input-----
The input consists of three integers:
a: The first integer.
b: The second integer.
c: The third integer.

-----Output-----
The output is an integer:
Returns the maximum of the three input numbers, assuring that the returned value is greater than or equal to a, b, and c, and that it matches one of these values.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (result >= a ∧ result >= b ∧ result >= c) ∧ (result = a ∨ result = b ∨ result = c)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U08

The function with its contract, comments removed:

```c
#include "pfc.h"
long myMin(long a, long b)
    ensures(result <= a && result <= b)
    ensures(result == a || result == b)
{
    if (a <= b) {
        return a;
    }
    return b;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that determines the minimum of two integers. The method should return the smaller of the two numbers. When both numbers are equal, either one may be returned.

-----Input-----
The input consists of two integers:
a: The first integer.
b: The second integer.

-----Output-----
The output is an integer:
Returns the smaller value between the input integers, ensuring that the result is less than or equal to both inputs.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (result ≤ a ∧ result ≤ b) ∧
  (result = a ∨ result = b)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U09

The function with its contract, comments removed:

```c
#include "pfc.h"
long SwapBitvectors(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == Y && out[1] == X)
    ensures(X == Y || (out[0] != X && out[1] != Y))
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
```

Verina's description:

```
-----Description-----  
This task requires swapping two 8-bit unsigned integers. Given two unsigned integer inputs, the goal is to produce an output pair where the first element is the original second input and the second element is the original first input. The problem focuses solely on exchanging the values without specifying any particular method to achieve the swap.

-----Input-----  
The input consists of:  
• X: A UInt8 value.  
• Y: A UInt8 value.

-----Output-----  
The output is a pair of UInt8 values (newX, newY) where:  
• newX is equal to the original Y.  
• newY is equal to the original X.

-----Note-----  
There are no additional preconditions; the function is meant to work correctly for any pair of UInt8 values by leveraging bitwise xor operations.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result.fst = Y ∧ result.snd = X ∧
  (X ≠ Y → result.fst ≠ X ∧ result.snd ≠ Y)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U10

The function with its contract, comments removed:

```c
#include "pfc.h"
long duo_code(long n, const int colors[n])
    requires(2 <= n && 0 <= colors[0] && colors[0] <= 9 && 0 <= colors[1] && colors[1] <= 9)
    ensures(result == colors[0] * 10 + colors[1])
{
    return (colors[0] * 10 + colors[1]);
}
```

Exercism's instructions:

```
# Instructions

If you want to build something using a Raspberry Pi, you'll probably use _resistors_.
For this exercise, you need to know two things about them:

- Each resistor has a resistance value.
- Resistors are small - so small in fact that if you printed the resistance value on them, it would be hard to read.

To get around this problem, manufacturers print color-coded bands onto the resistors to denote their resistance values.
Each band has a position and a numeric value.

The first 2 bands of a resistor have a simple encoding scheme: each color maps to a single number.
For example, if they printed a brown band (value 1) followed by a green band (value 5), it would translate to the number 15.

In this exercise you are going to create a helpful program so that you don't have to remember the values of the bands.
The program will take color names as input and output a two digit number, even if the input is more than two colors!

The band colors are encoded as follows:

- black: 0
- brown: 1
- red: 2
- orange: 3
- yellow: 4
- green: 5
- blue: 6
- violet: 7
- grey: 8
- white: 9

From the example above:
brown-green should return 15, and
brown-green-violet should return 15 too, ignoring the third color.
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U11

The function with its contract, comments removed:

```c
#include "pfc.h"
long Abs(long x)
    ensures((x < 0 || x == result) && (x >= 0 || x + result == 0))
{
    if (x < 0) {
        return -x;
    }
    return x;
}
```

Verina's description:

```
-----Description-----  
This task is about calculating the absolute value of an integer. The goal is to determine the non-negative value of a given integer: if the integer is non-negative, it remains unchanged; if it is negative, its positive counterpart is returned.

-----Input-----  
The input consists of:  
• x: An integer.

-----Output-----  
The output is an integer that represents the absolute value of the input. Specifically:  
• If x is non-negative, the output is x.  
• If x is negative, the output is the negation of x (that is, a value y such that x + y = 0).

-----Note-----  
This function should correctly handle zero, positive, and negative integers.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (x ≥ 0 → x = result) ∧ (x < 0 → x + result = 0)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U12

The function with its contract, comments removed:

```c
#include "pfc.h"
long isDivisibleBy11(long n)
    ensures((result == 1 && n % 11 == 0) || (result == 0 && n % 11 != 0))
{
    if (n % 11 == 0) {
        return 1;
    }
    return 0;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that determines whether a given integer is divisible by 11. The method should return true if the number is divisible by 11 and false otherwise.

-----Input-----
The input consists of:
n: An integer to check for divisibility by 11.

-----Output-----
The output is a Boolean value:
Returns true if the input number is divisible by 11.
Returns false if the input number is not divisible by 11.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (result → (∃ k : Int, n = 11 * k)) ∧ (¬ result → (∀ k : Int, ¬ n = 11 * k))
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U13

The function with its contract, comments removed:

```c
#include "pfc.h"
long singleDigitPrimeFactor(long n)
    requires(0 <= n)
    ensures(result == 0 || result == 2 || result == 3 || result == 5 || result == 7)
    ensures(result != 0 || n == 0 || (n % 2 != 0 && n % 3 != 0 && n % 5 != 0 && n % 7 != 0))
    ensures(result == 0 || (n != 0 && n % result == 0))
    ensures(result == 0 || ((result <= 2 || n % 2 != 0) && (result <= 3 || n % 3 != 0) && (result <= 5 || n % 5 != 0) && (result <= 7 || n % 7 != 0)))
{
    if (n == 0) {
        return 0;
    }
    if (n % 2 == 0) {
        return 2;
    }
    if (n % 3 == 0) {
        return 3;
    }
    if (n % 5 == 0) {
        return 5;
    }
    if (n % 7 == 0) {
        return 7;
    }
    return 0;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that given an natural number n, returns the smallest prime factor that is less than 10. If none exist, return 0

-----Input-----
The input consists of one natural number:
n: The main natural number.

-----Output-----
The output is an natural number:
Returns the smallest prime factor that is less than 10 or, if none exist, 0
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result ∈ [0, 2, 3, 5, 7] ∧
  (result = 0 → (n = 0 ∨ [2, 3, 5, 7].all (n % · ≠ 0))) ∧
  (result ≠ 0 → n ≠ 0 ∧ n % result == 0 ∧ (List.range result).all (fun x => x ∈ [2, 3, 5, 7] → n % x ≠ 0))
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U14

The function with its contract, comments removed:

```c
#include "pfc.h"
long Compare(long a, long b)
    ensures((a != b || result == 1) && (a == b || result == 0))
{
    if (a == b) {
        return 1;
    }
    return 0;
}
```

Verina's description:

```
-----Description-----
This task involves determining whether two integer values are equal. The goal is simply to compare the two provided numbers and indicate with a Boolean result whether they are the same.

-----Input-----
The input consists of two elements:
• a: An element of type Int.
• b: An element of type Int.

-----Output-----
The output is a Boolean:
• Returns true if a equals b.
• Returns false if a does not equal b.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (a = b → result = true) ∧ (a ≠ b → result = false)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U15

The function with its contract, comments removed:

```c
#include "pfc.h"
long isEven(long n)
    ensures((result == 1 && n % 2 == 0) || (result == 0 && n % 2 != 0))
{
    if (n % 2 == 0) {
        return 1;
    }
    return 0;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that determines whether a given integer is even. In other words, the method should return true if the number is even and false if the number is odd.

-----Input-----
The input consists of:
n: An integer.

-----Output-----
The output is a Boolean value:
Returns true if the input number is even.
Returns false if the input number is odd.

-----Note-----
There are no preconditions; the method will always work for any integer input.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (result → n % 2 = 0) ∧ (¬ result → n % 2 ≠ 0)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U16

The function with its contract, comments removed:

```c
#include "pfc.h"
long SwapArithmetic(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == Y && out[1] == X)
    ensures(X == Y || (out[0] != X && out[1] != Y))
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
```

Verina's description:

```
-----Description-----  
This problem involves swapping the values of two integers. Given two integers as inputs, the objective is to return the two numbers in reversed order.

-----Input-----  
The input consists of two integers:  
• X: The first integer.  
• Y: The second integer.

-----Output-----  
The output is a tuple of two integers (Int × Int) where:  
• The first element is equal to Y.  
• The second element is equal to X.

-----Note-----  
There are no restrictions on the input values. The function must correctly swap the inputs regardless of whether they are positive, negative, or zero.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result.1 = Y ∧ result.2 = X ∧
  (X ≠ Y → result.fst ≠ X ∧ result.snd ≠ Y)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U17

The function with its contract, comments removed:

```c
#include "pfc.h"
long SquareRoot(long N)
    requires(N >= 0)
    ensures(0 <= result && result * result <= N && N < (result + 1) * (result + 1))
{
    long r = 0;
    while ((r + 1) * (r + 1) <= N) invariant(0 <= r && r * r <= N) {
        r++;
    }
    return r;
}
```

Verina's description:

```
-----Description-----  
This task involves computing the integer square root of a given natural number. The goal is to determine the largest natural number r that satisfies r * r ≤ N and N < (r + 1) * (r + 1).

-----Input-----  
The input consists of:  
• N: A natural number.

-----Output-----  
The output is a natural number r that meets the following conditions:  
• r * r ≤ N  
• N < (r + 1) * (r + 1)

-----Note-----  
The implementation relies on a recursive strategy to iteratively increment r until (r + 1)*(r + 1) exceeds N. Edge cases, such as N = 0, should be handled correctly.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result * result ≤ N ∧ N < (result + 1) * (result + 1)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U18

The function with its contract, comments removed:

```c
#include "pfc.h"
long CalSum(long N)
    requires(N >= 0)
    ensures(2 * result == N * (N + 1))
{
    long sum = 0;
    for (long i = 1; i <= N; i++) invariant(1 <= i && i <= N + 1 && 2 * sum == (i - 1) * i) {
        sum += i;
    }
    return sum;
}
```

Verina's description:

```
-----Description-----
This problem asks for a method to determine the sum of the first N natural numbers. The task focuses on computing the total when given an input N, ensuring that the value is 0 when N is 0 and correctly calculated for positive values of N.

-----Input-----
The input consists of:
• N: A natural number (Nat) representing the count of the first natural numbers to sum.

-----Output-----
The output is a natural number (Nat), which is the sum of the first N natural numbers computed as: N * (N + 1) / 2.

-----Note-----
The computation leverages a recursive implementation. There are no additional preconditions beyond providing a valid natural number.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  2 * result = N * (N + 1)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U19

The function with its contract, comments removed:

```c
#include "pfc.h"
long myMin(long x, long y)
    ensures(x > y || result == x)
    ensures(x <= y || result == y)
{
    if (x <= y) {
        return x;
    }
    return y;
}
```

Verina's description:

```
-----Description-----  
This task requires determining the smaller of two integers. Given two input numbers, the goal is to compare them and return the one that is less than or equal to the other.

-----Input-----  
The input consists of two integers:  
• x: The first integer.  
• y: The second integer.

-----Output-----  
The output is an integer representing the minimum of the two input integers:  
• Returns x if x is less than or equal to y.  
• Returns y if x is greater than y.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (x ≤ y → result = x) ∧ (x > y → result = y)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U20

The function with its contract, comments removed:

```c
#include "pfc.h"
long multiply(long a, long b)
    ensures(result == a * b)
{
    return a * b;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that multiplies two integers. The method should return the product of the two input numbers.

-----Input-----
The input consists of:
a: The first integer.
b: The second integer.

-----Output-----
The output is an integer:
Returns the product of the two input integers (a * b).
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result - a * b = 0 ∧ a * b - result = 0
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U21

The function with its contract, comments removed:

```c
#include "pfc.h"
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    if (x == 0) {
        return 0;
    }
    return x + 2 * x;
}
```

Verina's description:

```
-----Description-----  
This task involves determining the triple of a given integer. The goal is to create a function that, for any integer provided as input, returns a value equal to three times that integer, including handling the case when the input is zero.

-----Input-----  
The input consists of:  
• x: An integer.

-----Output-----  
The output is an integer that represents three times the input integer.  
• If x = 0, the output will be 0.  
• Otherwise, the output will be computed as x + 2 * x, which is equivalent to 3 * x.

-----Note-----  
There are no additional preconditions. It is assumed that x is a valid integer.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result / 3 = x ∧ result / 3 * 3 = result
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U22

The function with its contract, comments removed:

```c
#include "pfc.h"
_Bool is_leap_year(long year)
    ensures(result == ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0))
{
    if (year % 4 == 0) {
        if (year % 400 == 0) {
            return 1;
        }
        if (year % 100 == 0) {
            return 0;
        }
        return 1;
    }
    return 0;
}
```

Exercism's introduction:

```
# Introduction

A leap year (in the Gregorian calendar) occurs:

- In every year that is evenly divisible by 4.
- Unless the year is evenly divisible by 100, in which case it's only a leap year if the year is also evenly divisible by 400.

Some examples:

- 1997 was not a leap year as it's not divisible by 4.
- 1900 was not a leap year as it's not divisible by 400.
- 2000 was a leap year!

~~~~exercism/note
For a delightful, four-minute explanation of the whole phenomenon of leap years, check out [this YouTube video](https://www.youtube.com/watch?v=xX96xng7sAE).
~~~~
```

Exercism's instructions:

```
# Instructions

Your task is to determine whether a given year is a leap year.
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U23

The function with its contract, comments removed:

```c
#include "pfc.h"
long DoubleQuadruple(long x, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == 2 * x && out[1] == 2 * out[0])
{
    out[0] = 2 * x;
    out[1] = 4 * x;
    return 0;
}
```

Verina's description:

```
-----Description-----  
Given an integer x, determine a pair (a, b) where the first element is twice the value of x and the second element is four times the value of x.

-----Input-----  
The input consists of:  
• x: An integer.

-----Output-----  
The output is a tuple (a, b) where:  
• a = 2 * x  
• b = 4 * x

-----Note-----  
There are no additional preconditions; the method is defined for all integers.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result.fst = 2 * x ∧ result.snd = 2 * result.fst
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U24

The function with its contract, comments removed:

```c
#include "pfc.h"
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    return 3 * x;
}
```

Verina's description:

```
-----Description-----
This task involves computing three times a given integer. Given an integer, the goal is to produce a value that is exactly three times its value.

-----Input-----
The input consists of a single integer:
x: An integer.

-----Output-----
The output is an integer:
Returns the product of the input integer and 3.

-----Note-----
There are no additional preconditions.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result / 3 = x ∧ result / 3 * 3 = result
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U25

The function with its contract, comments removed:

```c
#include "pfc.h"
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    return 3 * x;
}
```

Verina's description:

```
-----Description-----  
This task requires computing three times the given integer. The goal is to determine the product of the input integer and 3.

-----Input-----  
The input consists of:  
• x: An integer.

-----Output-----  
The output is an integer that represents three times the input value.

-----Note-----  
The implementation uses two different branches based on the value of x (i.e., x < 18 or x ≥ 18), but both branches guarantee that the result equals 3*x.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result / 3 = x ∧ result / 3 * 3 = result
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U26

The function with its contract, comments removed:

```c
#include "pfc.h"
#define ROW_COUNT 8
#define COLUMN_COUNT 8
#define CAN_NOT_ATTACK 0
#define CAN_ATTACK 1
#define INVALID_POSITION 2
long queens_attack(long white_row, long white_column, long black_row, long black_column)
    requires(0 <= white_row && white_row <= 255 && 0 <= white_column && white_column <= 255)
    requires(0 <= black_row && black_row <= 255 && 0 <= black_column && black_column <= 255)
    ensures(!((white_column == black_column && white_row == black_row) || white_row >= ROW_COUNT || white_column >= COLUMN_COUNT || black_row >= ROW_COUNT || black_column >= COLUMN_COUNT) || result == INVALID_POSITION)
    ensures(((white_column == black_column && white_row == black_row) || white_row >= ROW_COUNT || white_column >= COLUMN_COUNT || black_row >= ROW_COUNT || black_column >= COLUMN_COUNT) || !(white_column == black_column || white_row == black_row || white_row - black_row == white_column - black_column || white_row - black_row == black_column - white_column) || result == CAN_ATTACK)
    ensures(((white_column == black_column && white_row == black_row) || white_row >= ROW_COUNT || white_column >= COLUMN_COUNT || black_row >= ROW_COUNT || black_column >= COLUMN_COUNT) || (white_column == black_column || white_row == black_row || white_row - black_row == white_column - black_column || white_row - black_row == black_column - white_column) || result == CAN_NOT_ATTACK)
{
    if ((white_column == black_column && white_row == black_row) || white_row >= ROW_COUNT ||
        white_column >= COLUMN_COUNT || black_row >= ROW_COUNT || black_column >= COLUMN_COUNT) {
        return INVALID_POSITION;
    }
    if (white_column == black_column || white_row == black_row ||
        (white_row - black_row == white_column - black_column) ||
        (white_row - black_row == black_column - white_column)) {
        return CAN_ATTACK;
    }
    return CAN_NOT_ATTACK;
}
```

Exercism's instructions:

```
# Instructions

Given the position of two queens on a chess board, indicate whether or not they are positioned so that they can attack each other.

In the game of chess, a queen can attack pieces which are on the same row, column, or diagonal.

A chessboard can be represented by an 8 by 8 array.

So if you are told the white queen is at `c5` (zero-indexed at column 2, row 3) and the black queen at `f2` (zero-indexed at column 5, row 6), then you know that the set-up is like so:

![A chess board with two queens. Arrows emanating from the queen at c5 indicate possible directions of capture along file, rank and diagonal.](https://assets.exercism.org/images/exercises/queen-attack/queen-capture.svg)

You are also able to answer whether the queens can attack each other.
In this case, that answer would be yes, they can, because both pieces share a diagonal.

## Credit

The chessboard image was made by [habere-et-dispertire][habere-et-dispertire] using LaTeX and the [chessboard package][chessboard-package] by Ulrike Fischer.

[habere-et-dispertire]: https://exercism.org/profiles/habere-et-dispertire
[chessboard-package]: https://github.com/u-fischer/chessboard
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U27

The function with its contract, comments removed:

```c
#include "pfc.h"
long hasOppositeSign(long a, long b)
    ensures(!((a < 0 && b > 0) || (a > 0 && b < 0)) || result == 1)
    ensures(((a < 0 && b > 0) || (a > 0 && b < 0)) || result == 0)
{
    if ((a < 0 && b > 0) || (a > 0 && b < 0)) {
        return 1;
    }
    return 0;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that determines whether two given integers have opposite signs. In other words, the method should return true if one integer is positive and the other is negative. Note that zero is considered neither positive nor negative; therefore, if either integer is zero, the method should return false.

-----Input-----
The input consists of two integers:
a: An integer.
b: An integer.

-----Output-----
The output is a Boolean value:
Returns true if one of the integers is positive and the other is negative (i.e., they have opposite signs).
Returns false if both integers are either non-negative or non-positive, or if one (or both) is zero.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  (((a < 0 ∧ b > 0) ∨ (a > 0 ∧ b < 0)) → result) ∧
  (¬((a < 0 ∧ b > 0) ∨ (a > 0 ∧ b < 0)) → ¬result)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U28

The function with its contract, comments removed:

```c
#include "pfc.h"
long sumOfFourthPowerOfOddNumbers(long n)
    requires(n >= 0)
    ensures(15 * result == n * (2 * n + 1) * (7 + 24 * n * n * n - 12 * n * n - 14 * n))
{
    long sum = 0;
    for (long i = 0; i < n; i++) invariant(0 <= i && i <= n && 15 * sum == i * (2 * i + 1) * (7 + 24 * i * i * i - 12 * i * i - 14 * i)) decreases(n - i) {
        long odd = 2 * i + 1;
        sum += odd * odd * odd * odd;
    }
    return sum;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that computes the sum of the fourth power of the first n odd natural numbers. In other words, given a non-negative integer n, the method should calculate the sum: 1⁴ + 3⁴ + 5⁴ + ... for the first n odd numbers.

-----Input-----
The input consists of:
n: A non-negative natural number representing the number of odd natural numbers to consider.

-----Output----- 
The output is a natural number:
Returns the sum of the fourth power of the first n odd natural numbers.

-----Note----- 
The input n is assumed to be a non-negative integer.
The correctness of the result is established by a theorem that relates the computed sum to a specific formula.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  15 * result = n * (2 * n + 1) * (7 + 24 * n^3 - 12 * n^2 - 14 * n)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U29

The function with its contract, comments removed:

```c
#include "pfc.h"
long sumOfSquaresOfFirstNOddNumbers(long n)
    requires(n >= 0)
    ensures(result == (n * (2 * n - 1) * (2 * n + 1)) / 3)
{
    return (n * (2 * n - 1) * (2 * n + 1)) / 3;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that computes the sum of the squares of the first n odd natural numbers. The result should match the formula: (n * (2 * n - 1) * (2 * n + 1)) / 3.

-----Input-----
The input consists of:
n: A natural number representing the count of odd natural numbers to consider (n should be non-negative).

-----Output-----
The output is a natural number:
Returns the sum of the squares of the first n odd natural numbers, as defined by the formula: (n * (2 * n - 1) * (2 * n + 1)) / 3.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result - (n * (2 * n - 1) * (2 * n + 1)) / 3 = 0 ∧
  (n * (2 * n - 1) * (2 * n + 1)) / 3 - result = 0
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U30

The function with its contract, comments removed:

```c
#include "pfc.h"
long cubeSurfaceArea(long size)
    requires(size >= 0)
    ensures(result == 6 * size * size)
{
    return 6 * size * size;
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that calculates the surface area of a cube based on the length of one of its edges. The method should compute the surface area using the standard formula for a cube.

-----Input-----
The input consists of:
size: An natural number representing the length of an edge of the cube.

-----Output-----
The output is an natural number:
Returns the surface area of the cube.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result - 6 * size * size = 0 ∧ 6 * size * size - result = 0
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U31

The function with its contract, comments removed:

```c
#include "pfc.h"
long kthElement(long arr_len, const long arr[arr_len], long k)
    requires(1 <= k && k <= arr_len)
    ensures(result == arr[k - 1])
{
    return arr[k - 1];
}
```

Verina's description:

```
-----Description----- 
This task requires writing a Lean 4 method that finds the kth element in a given array using 1-based indexing. The method should return the element at the specified position, where the first element is at position 1.

-----Input-----
The input consists of:
arr: An array of integers.
k: An integer representing the position (1-based index) of the element to find.

-----Output-----
The output is an integer:
Returns the element at the kth position in the array.

-----Note-----
The input k is assumed to be valid (between 1 and array length inclusive).
The array is assumed to be non-empty.
```

Verina's precondition (Lean):

```lean
  k ≥ 1 ∧ k ≤ arr.size
```

Verina's postcondition (Lean):

```lean
  arr.any (fun x => x = result ∧ x = arr[k - 1]!)
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:

## U32

The function with its contract, comments removed:

```c
#include "pfc.h"
long MultipleReturns(long x, long y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == x + y && out[1] + y == x)
{
    out[0] = x + y;
    out[1] = x - y;
    return 0;
}
```

Verina's description:

```
-----Description-----  
Given two integers, the task is to compute two output values: one being the sum of the integers and the other being their difference.

-----Input-----  
The input consists of two integers:  
• x: An integer.  
• y: An integer.

-----Output-----  
The output is a tuple of two integers:  
• The first element is x + y.  
• The second element is x - y.

-----Note-----  
It is assumed that x and y are valid integers. There are no additional constraints on the inputs.
```

Verina's precondition (Lean):

```lean
  True
```

Verina's postcondition (Lean):

```lean
  result.1 = x + y ∧ result.2 + y = x
```

Answer: [ ] restates  [ ] different  [ ] unclear

Notes:
