#include "pfc.h"

/* Verina verina_basic_24: the first even element of a minus the first odd element. */
long firstEvenOddDifference(long a_len, const long a[a_len])
{
    long firstEven = 0;
    long firstOdd = 0;
    _Bool haveEven = 0;
    _Bool haveOdd = 0;

    for (long i = 0; i < a_len; i++) {
        if (a[i] % 2 == 0) {
            if (!haveEven) {
                firstEven = a[i];
                haveEven = 1;
            }
        } else {
            if (!haveOdd) {
                firstOdd = a[i];
                haveOdd = 1;
            }
        }
        if (haveEven && haveOdd) {
            break;
        }
    }
    return firstEven - firstOdd;
}
