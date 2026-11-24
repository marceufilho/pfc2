#include "pfc.h"
/* pfc-heldout-3b0ab9ca899f1e1ee4c6b425010fb1b3 */

long nr3(long volArray[], long volArray_len, long CELLCOUNT)
{
    REQUIRES(CELLCOUNT > 1 && CELLCOUNT <= volArray_len);
    long MINVAL = 2;
    long i = 0;
    long j = 0;
    i = 1;
    while (i <= CELLCOUNT / 3) {
        j = 3;
        while (j >= 1) {
            if (j >= MINVAL) {
                volArray[i * 3 - j] = j;
            } else {
                volArray[i * 3 - j] = 0;
            }
            j = j - 1;
        }
        i = i + 1;
    }
    return i;
}
