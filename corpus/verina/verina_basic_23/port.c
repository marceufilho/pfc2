#include "pfc.h"

/* Verina verina_basic_23: the largest element of a minus the smallest. */
long differenceMinMax(long a_len, const long a[a_len])
    requires(a_len >= 1)
    ensures(result >= 0)
{
    long lowest = a[0];
    long highest = a[0];

    for (long i = 1; i < a_len; i++) invariant(1 <= i && i <= a_len && lowest <= highest) decreases(a_len - i) {
        if (a[i] < lowest) {
            lowest = a[i];
        }
        if (a[i] > highest) {
            highest = a[i];
        }
    }
    return highest - lowest;
}
