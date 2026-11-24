#include "pfc.h"
/* pfc-heldout-53e905df044ee830b36619cc4fa3caeb */

long rew(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long val2 = 3;
    long val1 = 0;
    long i = 0;
    i = 0;
    while (i < SIZE) {
        if (i + 1 < SIZE) {
            a[i + 1] = val1;
        }
        a[i] = val2;
        i = i + 1;
    }
    return i;
}
