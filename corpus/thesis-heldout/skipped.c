#include "pfc.h"
/* pfc-heldout-0d6b2752dda2e106edbf85e24120047c */

long skipped(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long i = 0;
    i = 1;
    while (i <= SIZE / 2) {
        if (a[2 * i - 2] > 2 * i - 2) {
            a[2 * i - 2] = 2 * i - 2;
        }
        if (a[2 * i - 1] > 2 * i - 1) {
            a[2 * i - 1] = 2 * i - 1;
        }
        i = i + 1;
    }
    return i;
}
