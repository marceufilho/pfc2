/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu08(long v0, long v2, long v1)
{
    REQUIRES((((v0 >= 0) && (0 == v2)) && (0 == v1)));
    while ((v1 < v0)) {
        INVARIANT(((v2 >= 0) && (v1 >= 0)));
        v2 = (v1 + v2);
        v1 = (1 + v1);
    }
    ASSERT((v2 >= 0));
    return v2;
}
