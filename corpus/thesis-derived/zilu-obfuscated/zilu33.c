/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu33(long v0)
{
    REQUIRES((v0 >= 0));
    while (((v0 < 100) && (v0 >= 0))) {
        INVARIANT((v0 >= 0));
        v0 = (1 + v0);
    }
    ASSERT((v0 >= 100));
    return v0;
}
