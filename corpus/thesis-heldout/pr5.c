#include "pfc.h"
/* pfc-heldout-4155c5b1fb8d040112b1b3bad0474775 */

long pr5(long volArray[], long volArray_len, long CELLCOUNT, long MINVAL)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long CCCELVOL5 = 2;
    long CCCELVOL4 = 5;
    long CCCELVOL3 = 7;
    long CCCELVOL2 = 3;
    long CCCELVOL1 = 1;
    long i = 0;
    i = 1;
    while (i <= CELLCOUNT / 5) {
        if (CCCELVOL5 >= MINVAL) {
            volArray[i * 5 - 5] = CCCELVOL5;
        } else {
            volArray[i * 5 - 5] = 0;
        }
        if (CCCELVOL4 >= MINVAL) {
            volArray[i * 5 - 4] = CCCELVOL4;
        } else {
            volArray[i * 5 - 4] = 0;
        }
        if (CCCELVOL3 >= MINVAL) {
            volArray[i * 5 - 3] = CCCELVOL3;
        } else {
            volArray[i * 5 - 3] = 0;
        }
        if (CCCELVOL2 >= MINVAL) {
            volArray[i * 5 - 2] = CCCELVOL2;
        } else {
            volArray[i * 5 - 2] = 0;
        }
        if (CCCELVOL1 >= MINVAL) {
            volArray[i * 5 - 1] = CCCELVOL1;
        } else {
            volArray[i * 5 - 1] = 0;
        }
        i = i + 1;
    }
    return i;
}
