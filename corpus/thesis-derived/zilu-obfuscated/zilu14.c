/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu14(long v0)
{
    REQUIRES(((v0 >= 0) && (v0 <= 200)));
    while ((v0 > 0)) {
        INVARIANT((v0 >= 0));
        v0 = (v0 - 1);
    }
    ASSERT((v0 >= 0));
    return v0;
}
