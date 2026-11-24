#include "pfc.h"

_Bool is_leap_year(long year)
    ensures(result == ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0))
{
    if (year % 4 == 0) {
        if (year % 400 == 0) {
            return 1;
        }
        if (year % 100 == 0) {
            return 0;
        }
        return 1;
    }
    return 0;
}
