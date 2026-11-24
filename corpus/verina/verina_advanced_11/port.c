#include "pfc.h"

/* Verina verina_advanced_11: the element that appears more than half the time, or -1 when there is none. */
long findMajorityElement(long lst_len, const long lst[lst_len])
    /* The postcondition compares occurrence counts with lst_len / 2: not statable, dropped. */
{
    for (long i = 0; i < lst_len; i++) {
        long count = 0;
        for (long j = 0; j < lst_len; j++) invariant(0 <= count && count <= j) {
            if (lst[j] == lst[i]) {
                count++;
            }
        }
        if (count > lst_len / 2) {
            return lst[i];
        }
    }
    return -1;
}
