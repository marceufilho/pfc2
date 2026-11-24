#include "pfc.h"

/* Over mathematical integers k == i, so the access is in bounds. In C, `w * 2` can wrap and move k far
 * outside the array: the proof removes the bounds check only because that multiplication keeps its trap. */
long pick(long n, const long a[n], long i, long w)
    requires(0 <= i && i < n)
{
    long t = w * 2;
    long k = i + (t / 2 - w);
    return a[k];
}
