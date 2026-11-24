#include "pfc.h"
/* pfc-heldout-f27f6939e3f0d07432d2effeec1ba78d */

long revcpyswp2(long a[], long a_len, long b[], long b_len, const long a_copy[], long a_copy_len, const long b_copy[], long b_copy_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len && SIZE <= b_len && SIZE <= a_copy_len && SIZE <= b_copy_len);
    long i = 0;
    long tmp = 0;
    i = 0;
    while (i < SIZE) {
        a[i] = a_copy[SIZE - i - 1];
        b[i] = b_copy[SIZE - i - 1];
        i = i + 1;
    }
    i = 0;
    while (i < SIZE) {
        tmp = a[i];
        a[i] = b[i];
        b[i] = tmp;
        i = i + 1;
    }
    i = 0;
    while (i < SIZE) {
        tmp = a[i];
        a[i] = b[i];
        b[i] = tmp;
        i = i + 1;
    }
    return i;
}
