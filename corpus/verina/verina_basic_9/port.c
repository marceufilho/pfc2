#include "pfc.h"

/* Verina verina_basic_9: 1 when some element occurs in both a and b, else 0. */
long hasCommonElement(long a_len, const long a[a_len], long b_len, const long b[b_len])
    requires(a_len > 0 && b_len > 0)
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i < a_len; i++) {
        for (long j = 0; j < b_len; j++) {
            if (a[i] == b[j]) {
                return 1;
            }
        }
    }
    return 0;
}
