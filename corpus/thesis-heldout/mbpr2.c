#include "pfc.h"
/* pfc-heldout-5b33083a471fb5392d0dfdedb63f1f99 */

long mbpr2(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
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
        volArray[i * 2 - 1] = volArray[i * 2 - 1];
        i = i + 1;
    }
    i = 1;
    while (i <= CELLCOUNT / 2) {
        if (CCCELVOL1 >= MINVAL) {
            volArray[i * 2 - 1] = CCCELVOL1;
        } else {
            volArray[i * 2 - 1] = 0;
        }
        volArray[i * 2 - 2] = volArray[i * 2 - 2];
        i = i + 1;
    }
    return i;
}
