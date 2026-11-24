#include "pfc.h"
/* pfc-heldout-ebf4c5c4207ac72cc71671f01dc31ae3 */

long nr4(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
    long i = 0;
    long j = 0;
    i = 1;
    while (i <= CELLCOUNT / 4) {
        j = 4;
        while (j >= 1) {
            if (j >= MINVAL) {
                volArray[i * 4 - j] = j;
            } else {
                volArray[i * 4 - j] = 0;
            }
            j = j - 1;
        }
        i = i + 1;
    }
    return i;
}
