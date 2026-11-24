#include "pfc.h"
/* pfc-heldout-42e2c5733c95fbe44f446ce2765b9f3b */

long pr2(long volArray[], long volArray_len, long CELLCOUNT, long MINVAL)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long CCCELVOL2 = 3;
    long CCCELVOL1 = 1;
    long i = 0;
    i = 1;
    while (i <= CELLCOUNT / 2) {
        if (CCCELVOL2 >= MINVAL) {
            volArray[i * 2 - 2] = CCCELVOL2;
        } else {
            volArray[i * 2 - 2] = 0;
        }
        if (CCCELVOL1 >= MINVAL) {
            volArray[i * 2 - 1] = CCCELVOL1;
        } else {
            volArray[i * 2 - 1] = 0;
        }
        i = i + 1;
    }
    return i;
}
