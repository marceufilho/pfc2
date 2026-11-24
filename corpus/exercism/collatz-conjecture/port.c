#include "pfc.h"

#define ERROR_VALUE -1

/* Number of Collatz steps from `start` to 1, or ERROR_VALUE. Upstream `int` becomes `long` (P1). */
long collatz_steps(long start)
    ensures(start > 0 || result == ERROR_VALUE)
    ensures(start <= 0 || result >= 0)
    ensures(start != 1 || result == 0)
{
    long step = 0;
    long number = start;

    if (start <= 0) {
        return ERROR_VALUE;
    }
    while (number != 1) invariant(0 <= step && 1 <= number && (start != 1 || (number == 1 && step == 0))) {
        step++;
        if (number % 2 == 0) {
            number /= 2;
        } else {
            number = (number * 3) + 1;
        }
    }
    return step;
}
