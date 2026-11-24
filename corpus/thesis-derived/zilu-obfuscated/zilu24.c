/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu24(long v0, long v2, long v1)
{
    REQUIRES((((0 == v0) && (v1 == v2)) && (v1 >= 0)));
    while ((v0 < v1)) {
        INVARIANT((((v1 * 2) == (v0 + (v2 * 2))) && (v0 <= (1 + v1))));
        v2 = (v2 - 1);
        v0 = (2 + v0);
    }
    ASSERT(((v2 * 2) >= (v1 - 1)));
    return v2;
}
