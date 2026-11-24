#include "pfc.h"
/* pfc-heldout-b045b1a7dda18b48b607680e7cd3a05c */

long nr5(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
    long i = 0;
    long j = 0;
    i = 1;
    while (i <= CELLCOUNT / 5) {
        j = 5;
        while (j >= 1) {
            if (j >= MINVAL) {
                volArray[i * 5 - j] = j;
            } else {
                volArray[i * 5 - j] = 0;
            }
            j = j - 1;
        }
        i = i + 1;
    }
    return i;
}
