#include "pfc.h"
/* pfc-heldout-73ad334d918f8f8356177156c3be9f92 */

long pnr2(const long port[], long port_len, long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len && SIZE <= port_len);
    long DEFAULTVAL = 0;
    long FIXEDVAL = 10;
    long value = 0;
    long i = 0;
    i = 1;
    while (i <= SIZE / 2) {
        value = port[i * 2 - 2];
        if (value != DEFAULTVAL) {
            a[i * 2 - 2] = value;
        } else {
            a[i * 2 - 2] = FIXEDVAL;
        }
        value = port[i * 2 - 1];
        if (value != DEFAULTVAL) {
            a[i * 2 - 1] = value;
        } else {
            a[i * 2 - 1] = FIXEDVAL;
        }
        i = i + 1;
    }
    return i;
}
