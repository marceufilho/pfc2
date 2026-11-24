#include "pfc.h"

/* Verina verina_advanced_40: the largest element of a non-empty list. */
long maxOfList(long lst_len, const long lst[lst_len])
    requires(lst_len > 0)
    /* result in lst and forall x in lst, x <= result: both quantified, dropped. Only the two end elements
     * of the bound are stated. */
    ensures(result >= lst[0] && result >= lst[lst_len - 1])
{
    long best = lst[0];

    for (long i = 1; i < lst_len; i++) invariant(best >= lst[0] && best >= lst[i - 1]) {
        if (lst[i] > best) {
            best = lst[i];
        }
    }
    return best;
}
