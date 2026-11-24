#include "pfc.h"

/* Verina verina_advanced_12: the first value, scanning left to right, that already appeared earlier.
 * out[0] is 1 and out[1] the value when there is one; out[0] is 0 otherwise. */
long firstDuplicate(long lst_len, const long lst[lst_len], long out_cap, long out[out_cap])
    requires(out_cap >= 2)
{
    for (long j = 0; j < lst_len; j++) {
        for (long i = 0; i < j; i++) {
            if (lst[i] == lst[j]) {
                out[0] = 1;
                out[1] = lst[j];
                return 0;
            }
        }
    }
    out[0] = 0;
    return 0;
}
