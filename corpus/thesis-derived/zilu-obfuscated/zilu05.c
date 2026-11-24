/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu05(long v0, long v2, long v1)
{
    REQUIRES((((v0 >= 0) && (v0 <= v2)) && (v2 < v1)));
    while ((v0 < v1)) {
        INVARIANT(((v0 <= v2) && (v2 <= v1)));
        v0 = (1 + v0);
        if ((v0 > v2)) {
            v2 = (1 + v2);
        }
    }
    ASSERT((v1 == v2));
    return v2;
}
