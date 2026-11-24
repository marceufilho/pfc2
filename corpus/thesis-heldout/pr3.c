#include "pfc.h"
/* pfc-heldout-5d1c78daea40a380e0b4df4e81b6e9dc */

long pr3(long volArray[], long volArray_len, long CELLCOUNT, long MINVAL)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
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
        if (CCCELVOL2 >= MINVAL) {
            volArray[i * 3 - 2] = CCCELVOL2;
        } else {
            volArray[i * 3 - 2] = 0;
        }
        if (CCCELVOL1 >= MINVAL) {
            volArray[i * 3 - 1] = CCCELVOL1;
        } else {
            volArray[i * 3 - 1] = 0;
        }
        i = i + 1;
    }
    return i;
}
