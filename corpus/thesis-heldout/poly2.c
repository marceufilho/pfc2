#include "pfc.h"
/* pfc-heldout-f1f86eb918026e46ebebc565c34df7e6 */

long poly2(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long i = 0;
    i = 0;
    while (i < SIZE) {
        a[i] = i * i + 2;
        i = i + 1;
    }
    i = 0;
    while (i < SIZE) {
        a[i] = a[i] - 2;
        i = i + 1;
    }
    return i;
}
