/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu06(long v3, long v2, long v1, long v5, long v0)
{
    REQUIRES(((v5 == (v1 + v2)) && (0 <= v0)));
    long v4 = 0;
    long v6 = 0;
    while ((v6 < v0)) {
        INVARIANT((v5 == (v1 + v2)));
        if (v3 == v4) {
            v2 = (1 + v2);
            v1 = (v1 - 1);
        } else {
            v1 = (1 + v1);
            v2 = (v2 - 1);
        }
        v4 = (1 + v4);
        v6 = (1 + v6);
    }
    ASSERT((v5 == (v1 + v2)));
    return v2;
}
