#include "pfc.h"

/* Verina verina_basic_68: index of the first occurrence of e in a, or the length of a when absent. */
long LinearSearch(long a_len, const long a[a_len], long e)
{
    for (long i = 0; i < a_len; i++) {
        if (a[i] == e) {
            return i;
        }
    }
    return a_len;
}
