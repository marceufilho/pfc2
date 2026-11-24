#include "pfc.h"

long count(long n where(0 <= n)) where(RESULT == n)
{
    long i where(0 <= i && i <= n) = 0;

    while (i < n) {
        i = i + 1;
    }
    return i;
}
