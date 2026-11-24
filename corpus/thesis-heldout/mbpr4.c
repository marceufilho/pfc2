#include "pfc.h"
/* pfc-heldout-15f4fa4a1e4c2d241fc3eddadc34948c */

long mbpr4(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
    long CCCELVOL4 = 5;
    long CCCELVOL3 = 7;
    long CCCELVOL2 = 3;
    long CCCELVOL1 = 1;
    long i = 0;
    i = 1;
    while (i <= CELLCOUNT / 4) {
        if (CCCELVOL4 >= MINVAL) {
            volArray[i * 4 - 4] = CCCELVOL4;
        } else {
            volArray[i * 4 - 4] = 0;
        }
        volArray[i * 4 - 3] = volArray[i * 4 - 3];
        volArray[i * 4 - 2] = volArray[i * 4 - 2];
        volArray[i * 4 - 1] = volArray[i * 4 - 1];
        i = i + 1;
    }
    i = 1;
    while (i <= CELLCOUNT / 4) {
        if (CCCELVOL3 >= MINVAL) {
            volArray[i * 4 - 3] = CCCELVOL3;
        } else {
            volArray[i * 4 - 3] = 0;
        }
        volArray[i * 4 - 4] = volArray[i * 4 - 4];
        volArray[i * 4 - 2] = volArray[i * 4 - 2];
        volArray[i * 4 - 1] = volArray[i * 4 - 1];
        i = i + 1;
    }
    i = 1;
    while (i <= CELLCOUNT / 4) {
        if (CCCELVOL2 >= MINVAL) {
            volArray[i * 4 - 2] = CCCELVOL2;
        } else {
            volArray[i * 4 - 2] = 0;
        }
        volArray[i * 4 - 4] = volArray[i * 4 - 4];
        volArray[i * 4 - 3] = volArray[i * 4 - 3];
        volArray[i * 4 - 1] = volArray[i * 4 - 1];
        i = i + 1;
    }
    i = 1;
    while (i <= CELLCOUNT / 4) {
        if (CCCELVOL1 >= MINVAL) {
            volArray[i * 4 - 1] = CCCELVOL1;
        } else {
            volArray[i * 4 - 1] = 0;
        }
        volArray[i * 4 - 4] = volArray[i * 4 - 4];
        volArray[i * 4 - 3] = volArray[i * 4 - 3];
        volArray[i * 4 - 2] = volArray[i * 4 - 2];
        i = i + 1;
    }
    return i;
}
