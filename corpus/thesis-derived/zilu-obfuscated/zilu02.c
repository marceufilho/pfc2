/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu02(long v0, long v2)
{
    REQUIRES((v2 > 0));
    long v1 = v2;
    while ((v1 < v0)) {
        INVARIANT((v2 > 0));
        v1 = (1 + v1);
    }
    ASSERT((v2 >= 1));
    return v1;
}
