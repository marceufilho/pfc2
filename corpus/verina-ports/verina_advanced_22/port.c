#include "pfc.h"

/* Verina verina_advanced_22: 1 when lst strictly increases and then strictly decreases, both parts
 * non-empty; else 0. */
long isPeakValley(long lst_len, const long lst[lst_len])
{
    long i = 1;

    while (i < lst_len && lst[i] > lst[i - 1]) {
        i++;
    }
    if (i == 1 || i >= lst_len) {
        return 0;
    }
    while (i < lst_len && lst[i] < lst[i - 1]) {
        i++;
    }
    if (i == lst_len) {
        return 1;
    }
    return 0;
}
