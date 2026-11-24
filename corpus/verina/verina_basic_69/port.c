#include "pfc.h"

/* Verina verina_basic_69: index of the first occurrence of e in a (e is assumed to occur). */
long LinearSearch(long a_len, const long a[a_len], long e)
    requires(a_len >= 0)
    ensures(0 <= result && result <= a_len)
    ensures(result == a_len || a[result] == e)
{
    long n = 0;

    while (n < a_len && a[n] != e) invariant(0 <= n && n <= a_len) {
        n++;
    }
    return n;
}
