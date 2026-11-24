#include "pfc.h"
/* pfc-heldout-f54480603a874aa11971b6e66d53617d */

long rewrev(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long val2 = 3;
    long val1 = 7;
    long i = 0;
    i = SIZE - 2;
    while (i >= -1) {
        if (i >= 0) {
            a[i] = val1;
        }
        a[i + 1] = val2;
        i = i - 1;
    }
    return i;
}
