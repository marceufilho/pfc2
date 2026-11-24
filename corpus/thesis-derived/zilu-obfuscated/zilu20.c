/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu20(long v0, long v2, long v1)
{
    REQUIRES(((((0 == v0) && (v2 >= 0)) && (v2 <= 100)) && (0 == v1)));
    while ((v0 < v2)) {
        INVARIANT(((v1 >= 0) && (v0 >= 0)));
        v1 = (v0 + v1);
        v0 = (1 + v0);
    }
    ASSERT((v1 >= 0));
    return v1;
}
