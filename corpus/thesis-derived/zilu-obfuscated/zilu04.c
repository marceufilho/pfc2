/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu04(long v0, long v2, long v1)
{
    REQUIRES((((v1 >= 1) && (v0 >= v1)) && (0 == v2)));
    while ((v2 <= (v1 - 1))) {
        INVARIANT((((v2 + v0) >= v1) && (v2 <= v1)));
        v2 = (1 + v2);
        v0 = (v0 - 1);
    }
    ASSERT((v0 >= 0));
    return v0;
}
