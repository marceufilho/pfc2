#include "pfc.h"

/* Verina verina_basic_69: index of the first occurrence of e in a (e is assumed to occur). */
long LinearSearch(long a_len, const long a[a_len], long e)
{
    long n = 0;

    while (n < a_len && a[n] != e) {
        n++;
    }
    return n;
}
