#include "pfc.h"

/* Nothing bounds the elements, so `s += a[i]` may overflow. The file certifies at --level memory:
 * every access is proved in bounds and the addition keeps its overflow trap, which is listed. */
long sum(long n, const long a[n])
{
    long s = 0;

    for (long i = 0; i < n; i++) {
        s += a[i];
    }
    return s;
}
