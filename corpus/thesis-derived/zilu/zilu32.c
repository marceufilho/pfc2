#include "pfc.h"

long zilu32(long x, long steps)
{
    REQUIRES((x == 1 || x == 2) && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(x == 1 || x == 2);
        if (x == 1) {
            x = 2;
        } else {
            if (x == 2) {
                x = 1;
            }
        }
        step = step + 1;
    }
    ASSERT(x <= 8);
    return x;
}
