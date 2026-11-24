#include "pfc.h"

/* Verina verina_basic_21: 1 when sub appears as a contiguous run inside main, else 0. */
long isSublist(long sub_len, const long sub[sub_len], long main_len, const long main[main_len])
    requires(main_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= main_len */
    requires(sub_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= sub_len */
    ensures(result == 0 || result == 1)
    ensures(sub_len != 0 || result == 1)
    ensures(sub_len <= main_len || result == 0)
{
    for (long start = 0; start + sub_len <= main_len; start++) invariant(0 <= start && (sub_len != 0 || start == 0)) {
        long k = 0;

        while (k < sub_len && sub[k] == main[start + k]) invariant(0 <= k && k <= sub_len) {
            k++;
        }
        if (k == sub_len) {
            return 1;
        }
    }
    return 0;
}
