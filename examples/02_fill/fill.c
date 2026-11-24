#include "pfc.h"

/* `long a[n]` says the array has n elements, so no length is passed by hand and every write is
 * proved inside the array: the certified C has no bounds check left. */
long fill(long n, long a[n], long value)
{
    for (long i = 0; i < n; i++) {
        a[i] = value;
    }
    return n;
}
