/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu15(long v0, long v2, long v1)
{
    REQUIRES((((0 == v0) && (v2 >= 1)) && ((v2 * 2) == v1)));
    while ((v2 > 0)) {
        INVARIANT(((((v2 * 2) + v0) == v1) && (v2 >= 0)));
        v0 = (1 + v0);
        v1 = (v1 - 1);
        v2 = (v2 - 1);
    }
    ASSERT((v1 == v0));
    return v0;
}
