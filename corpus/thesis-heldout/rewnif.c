#include "pfc.h"
/* pfc-heldout-a3cdb4fcdb2dcc5e41a896ab95b3d87d */

long rewnif(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long i = 0;
    i = 0;
    while (i < SIZE) {
        if (i + 1 < SIZE) {
            a[i + 1] = i;
        }
        a[i] = i;
        i = i + 1;
    }
    return i;
}
