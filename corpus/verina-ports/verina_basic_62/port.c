#include "pfc.h"

/* Verina verina_basic_62: index of the first occurrence of key in a, or -1. */
long Find(long a_len, const long a[a_len], long key)
{
    for (long i = 0; i < a_len; i++) {
        if (a[i] == key) {
            return i;
        }
    }
    return -1;
}
