#include "pfc.h"
/* pfc-heldout-2fe41690765f5fa16a5e54ba59fb7dcd */

long tcpy(const long a[], long a_len, long acopy[], long acopy_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len && SIZE <= acopy_len);
    long i = 0;
    i = 0;
    while (i < SIZE / 2) {
        acopy[SIZE - i - 1] = a[SIZE - i - 1];
        acopy[i] = a[i];
        i = i + 1;
    }
    return i;
}
