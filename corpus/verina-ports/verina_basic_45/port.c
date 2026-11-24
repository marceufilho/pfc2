#include "pfc.h"

/* Verina verina_basic_45: product of the first even and the first odd number of lst. */
long findProduct(long lst_len, const long lst[lst_len])
{
    long even = 0;
    long odd = 0;
    _Bool have_even = 0;
    _Bool have_odd = 0;

    for (long i = 0; i < lst_len; i++) {
        if (lst[i] % 2 == 0) {
            if (!have_even) {
                even = lst[i];
                have_even = 1;
            }
        } else {
            if (!have_odd) {
                odd = lst[i];
                have_odd = 1;
            }
        }
        if (have_even && have_odd) {
            break;
        }
    }
    return even * odd;
}
