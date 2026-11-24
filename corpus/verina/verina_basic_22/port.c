#include "pfc.h"

/* Verina verina_basic_22: the distinct values that are in exactly one of a and b, in ascending order. */
long contains(long n, const long xs[n], long value)
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i < n; i++) {
        if (xs[i] == value) {
            return 1;
        }
    }
    return 0;
}

long insertSorted(long count, long out_cap, long out[out_cap], long value)
    requires(0 <= count && count < out_cap)
    ensures(result == count || result == count + 1)
{
    long pos = 0;

    while (pos < count && out[pos] < value) invariant(0 <= pos && pos <= count) {
        pos++;
    }
    if (pos < count && out[pos] == value) {
        return count;
    }
    for (long j = count; j > pos; j--) invariant(pos <= j && j <= count) {
        out[j] = out[j - 1];
    }
    out[pos] = value;
    return count + 1;
}

long dissimilarElements(long a_len, const long a[a_len], long b_len, const long b[b_len], long out_cap, long out[out_cap])
    requires(b_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= b_len */
    requires(a_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= a_len */
    requires(out_cap >= a_len + b_len)
    ensures(0 <= result && result <= a_len + b_len)
{
    long count = 0;

    for (long i = 0; i < a_len; i++) invariant(0 <= i && i <= a_len && 0 <= count && count <= i) {
        long value = a[i];
        long inOther = contains(b_len, b, value);

        if (inOther == 0) {
            count = insertSorted(count, out_cap, out, value);
        }
    }
    for (long i = 0; i < b_len; i++) invariant(0 <= i && i <= b_len && 0 <= count && count <= a_len + i) {
        long value = b[i];
        long inOther = contains(a_len, a, value);

        if (inOther == 0) {
            count = insertSorted(count, out_cap, out, value);
        }
    }
    return count;
}
