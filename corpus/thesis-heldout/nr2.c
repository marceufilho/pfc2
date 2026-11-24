#include "pfc.h"
/* pfc-heldout-ff1a6ff15fd8c9bfdf5ed113a6df6aab */

long nr2(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
    long i = 0;
    long j = 0;
    i = 1;
    while (i <= CELLCOUNT / 2) {
        j = 2;
        while (j >= 1) {
            if (j >= MINVAL) {
                volArray[i * 2 - j] = j;
            } else {
                volArray[i * 2 - j] = 0;
            }
            j = j - 1;
        }
        i = i + 1;
    }
    return i;
}
