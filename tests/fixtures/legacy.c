#include "pfc.h"

long clamp(long x)
{
    ENSURES(0 <= RESULT && RESULT <= 100);
    if (x < 0) {
        return 0;
    }
    if (x > 100) {
        return 100;
    }
    return x;
}
