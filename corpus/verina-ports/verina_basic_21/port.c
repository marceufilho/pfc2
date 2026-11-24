#include "pfc.h"

/* Verina verina_basic_21: 1 when sub appears as a contiguous run inside main, else 0. */
long isSublist(long sub_len, const long sub[sub_len], long main_len, const long main[main_len])
{
    for (long start = 0; start + sub_len <= main_len; start++) {
        long k = 0;

        while (k < sub_len && sub[k] == main[start + k]) {
            k++;
        }
        if (k == sub_len) {
            return 1;
        }
    }
    return 0;
}
