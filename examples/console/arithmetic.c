#include "pfc.h"
#include "pfc_rt.h"

/* A chain of small arithmetic functions over a global. Each function states the range it is used with,
 * so every operation is proved free of overflow and the division proved not to divide by zero; `main`
 * then proves, by the contracts alone, that the chain ends at 10. */
long outcome = 0;

long add(long x, long y)
    requires(-1000000 <= x && x <= 1000000 && -1000000 <= y && y <= 1000000)
    ensures(result == x + y)
{
    return x + y;
}

long subtract(long x, long y)
    requires(-1000000 <= x && x <= 1000000 && -1000000 <= y && y <= 1000000)
    ensures(result == x - y)
{
    return x - y;
}

long multiply(long x, long y)
    requires(-1000000 <= x && x <= 1000000 && -1000000 <= y && y <= 1000000)
    ensures(result == x * y)
{
    return x * y;
}

long divide(long x, long y)
    requires(-1000000 <= x && x <= 1000000)
    ensures(y == 0 || result == x / y)
    ensures(y != 0 || result == 0)
{
    if (y == 0) {
        return 0;
    }
    return x / y;
}

long max(long x, long y)
    ensures(result >= x && result >= y && (result == x || result == y))
{
    if (x > y) {
        return x;
    }
    return y;
}

long min(long x, long y)
    ensures(result <= x && result <= y && (result == x || result == y))
{
    if (x < y) {
        return x;
    }
    return y;
}

int main(void)
{
    long a = 20;
    long b = 5;

    outcome = add(a, b);
    outcome = subtract(outcome, 3);
    outcome = multiply(outcome, 2);
    outcome = divide(outcome, b);
    outcome = max(outcome, 10);
    outcome = min(outcome, 50);
    assert(outcome == 10);
    print_int(outcome);
    println();
    return 0;
}
