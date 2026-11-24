#include "pfc.h"

#define ERROR_VALUE -1

/* Number of Collatz steps from `start` to 1, or ERROR_VALUE. Upstream `int` becomes `long` (P1). */
long collatz_steps(long start)
{
    long step = 0;
    long number = start;

    if (start <= 0) {
        return ERROR_VALUE;
    }
    while (number != 1) {
        step++;
        if (number % 2 == 0) {
            number /= 2;
        } else {
            number = (number * 3) + 1;
        }
    }
    return step;
}
