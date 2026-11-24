#include "pfc.h"

/* isdigit of the C locale, written out (P7). */
_Bool is_digit(long c)
{
    return c >= '0' && c <= '9';
}

/* Is `num` valid by the Luhn formula. The string arrives with its length (P2); upstream's `?:` is an `if`
 * (P6); the element is read into a local before the call (P13). */
_Bool luhn_valid(long n, const char num[n])
{
    long pos = n - 1;

    if (pos < 0) {
        return 0;
    }
    long res = 0;
    long every_second = 0;
    long zeros = 0;

    while (pos >= 0) {
        long current = num[pos];

        if (is_digit(current)) {
            long c = current - '0';

            zeros += (c == 0);
            if (every_second) {
                c *= 2;
                if (c > 9) {
                    res += c - 9;
                } else {
                    res += c;
                }
            } else {
                res += c;
            }
            every_second = !every_second;
        } else if (current != ' ') {
            return 0;
        }
        pos--;
    }
    if (res == 0 && zeros == 1) {
        return 0;
    }
    return (res % 10 == 0);
}
