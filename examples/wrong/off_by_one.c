#include "pfc.h"

/* `i <= n` writes one element past the end. Refused: the write at line 7 is not proved in bounds. */
long fill(long n, long a[n], long value)
{
    for (long i = 0; i <= n; i++) {
        a[i] = value;
    }
    return n;
}
