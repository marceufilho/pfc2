#include "pfc.h"

/* Verina verina_advanced_81: the distinct elements of arr in ascending order, written to out. */
long uniqueSorted(long arr_len, const long arr[arr_len], long out_cap, long out[out_cap])
    requires(out_cap >= arr_len)
{
    long count = 0;

    for (long i = 0; i < arr_len; i++) {
        long value = arr[i];
        long pos = 0;

        while (pos < count && out[pos] < value) {
            pos++;
        }
        if (pos < count && out[pos] == value) {
            continue;
        }
        for (long j = count; j > pos; j--) {
            out[j] = out[j - 1];
        }
        out[pos] = value;
        count++;
    }
    return count;
}
