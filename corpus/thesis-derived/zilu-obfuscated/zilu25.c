/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu25(long v0)
{
    REQUIRES((v0 < 0));
    while ((v0 < 10)) {
        INVARIANT((v0 <= 10));
        v0 = (1 + v0);
    }
    ASSERT((10 == v0));
    return v0;
}
