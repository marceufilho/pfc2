#include "pfc.h"

/* Verina verina_advanced_39: the largest element of a non-empty list. */
long maxOfList(long lst_len, const long lst[lst_len])
    requires(lst_len > 0)
{
    long best = lst[0];

    for (long i = 1; i < lst_len; i++) {
        if (lst[i] > best) {
            best = lst[i];
        }
    }
    return best;
}
