/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu32(long v0, long v2)
{
    REQUIRES((((1 == v0) || (2 == v0)) && (0 <= v2)));
    long v1 = 0;
    while ((v1 < v2)) {
        INVARIANT(((1 == v0) || (2 == v0)));
        if (1 == v0) {
            v0 = 2;
        } else {
            if (2 == v0) {
                v0 = 1;
            }
        }
        v1 = (1 + v1);
    }
    ASSERT((v0 <= 8));
    return v0;
}
