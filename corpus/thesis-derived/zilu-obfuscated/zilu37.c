/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu37(long v0, long v1)
{
    REQUIRES(((v1 == v0) && (v0 >= 0)));
    while ((v0 > 0)) {
        INVARIANT(((v1 == v0) && (v0 >= 0)));
        v0 = (v0 - 1);
        v1 = (v1 - 1);
    }
    ASSERT((v1 >= 0));
    return v1;
}
