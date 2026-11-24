#include "pfc.h"

#define PERFECT_NUMBER 1
#define ABUNDANT_NUMBER 2
#define DEFICIENT_NUMBER 3
#define ERROR -1

/* Upstream's local is called `result`, a word of the language; here it is `total`. Its `?:` is an `if` (P6). */
long aliquot_sum(long n)
    requires(1 <= n && n <= 2147483647)
    ensures(0 <= result && (n != 1 || result == 0) && (n == 1 || result >= 1))
{
    if (n == 1) {
        return 0;
    }
    long total = 1;
    long i = 2;

    for (i = 2; i * i < n; ++i) invariant(2 <= i && i <= 46342 && (i - 1) * (i - 1) <= n && 1 <= total && total <= 1 + (i - 2) * n) {
        if ((n % i) == 0) {
            total += i + (n / i);
        }
    }
    if (i * i == n) {
        return total + i;
    }
    return total + 0;
}

/* The enum becomes named constants (P5). */
long classify(long n)
    requires(-2147483647 - 1 <= n && n <= 2147483647)
    ensures(n > 0 || result == ERROR)
    ensures(n <= 0 || result == PERFECT_NUMBER || result == ABUNDANT_NUMBER || result == DEFICIENT_NUMBER)
    ensures(n != 1 || result == DEFICIENT_NUMBER)
{
    long class = ERROR;

    if (n > 0) {
        long sum = aliquot_sum(n);

        if (sum > n) {
            class = ABUNDANT_NUMBER;
        } else if (sum < n) {
            class = DEFICIENT_NUMBER;
        } else {
            class = PERFECT_NUMBER;
        }
    }
    return class;
}
