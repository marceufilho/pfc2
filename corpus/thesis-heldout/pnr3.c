#include "pfc.h"
/* pfc-heldout-2ecc867aeeb8b7d40dc8dd3ac25e9b44 */

long pnr3(const long port[], long port_len, long a[], long a_len, long SIZE)
{
    REQUIRES(SIZE > 1 && SIZE < 100000L && SIZE <= a_len && SIZE <= port_len);
    long DEFAULTVAL = 0;
    long FIXEDVAL = 10;
    long value = 0;
    long i = 0;
    i = 1;
    while (i <= SIZE / 3) {
        value = port[i * 3 - 3];
        if (value != DEFAULTVAL) {
            a[i * 3 - 3] = value;
        } else {
            a[i * 3 - 3] = FIXEDVAL;
        }
        value = port[i * 3 - 2];
        if (value != DEFAULTVAL) {
            a[i * 3 - 2] = value;
        } else {
            a[i * 3 - 2] = FIXEDVAL;
        }
        value = port[i * 3 - 1];
        if (value != DEFAULTVAL) {
            a[i * 3 - 1] = value;
        } else {
            a[i * 3 - 1] = FIXEDVAL;
        }
        i = i + 1;
    }
    return i;
}
