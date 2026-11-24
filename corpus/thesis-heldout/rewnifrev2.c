#include "pfc.h"
/* pfc-heldout-097b9f08352018aab5b8bb0f47a91328 */

long rewnifrev2(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long i = 0;
    i = SIZE - 2;
    while (i >= 0) {
        a[i] = i;
        a[i + 1] = i + 1;
        i = i - 1;
    }
    return i;
}
