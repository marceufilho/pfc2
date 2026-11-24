#include "pfc.h"
/* pfc-heldout-d3664347576d099cc39df1c9a76057f8 */

long rewnifrev(long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len);
    long i = 0;
    i = SIZE - 1;
    while (i >= 0) {
        if (i - 1 >= 0) {
            a[i - 1] = i - 2;
        }
        a[i] = i;
        i = i - 1;
    }
    return i;
}
