#include "pfc.h"
/* pfc-heldout-5d833c582579325292a9cebee7dc25a7 */

long mbpr3(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
    long CCCELVOL3 = 7;
    long CCCELVOL2 = 3;
    long CCCELVOL1 = 1;
    long i = 0;
    i = 1;
    while (i <= CELLCOUNT / 3) {
        if (CCCELVOL3 >= MINVAL) {
            volArray[i * 3 - 3] = CCCELVOL3;
        } else {
            volArray[i * 3 - 3] = 0;
        }
        volArray[i * 3 - 2] = volArray[i * 3 - 2];
        volArray[i * 3 - 1] = volArray[i * 3 - 1];
        i = i + 1;
    }
    i = 1;
    while (i <= CELLCOUNT / 3) {
        if (CCCELVOL2 >= MINVAL) {
            volArray[i * 3 - 2] = CCCELVOL2;
        } else {
            volArray[i * 3 - 2] = 0;
        }
        volArray[i * 3 - 3] = volArray[i * 3 - 3];
        volArray[i * 3 - 1] = volArray[i * 3 - 1];
        i = i + 1;
    }
    i = 1;
    while (i <= CELLCOUNT / 3) {
        if (CCCELVOL1 >= MINVAL) {
            volArray[i * 3 - 1] = CCCELVOL1;
        } else {
            volArray[i * 3 - 1] = 0;
        }
        volArray[i * 3 - 2] = volArray[i * 3 - 2];
        volArray[i * 3 - 3] = volArray[i * 3 - 3];
        i = i + 1;
    }
    return i;
}
