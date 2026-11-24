/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu35(long v0)
{
    REQUIRES((v0 >= 0));
    while (((v0 >= 0) && (v0 < 10))) {
        INVARIANT((v0 >= 0));
        v0 = (1 + v0);
    }
    ASSERT((v0 >= 10));
    return v0;
}
