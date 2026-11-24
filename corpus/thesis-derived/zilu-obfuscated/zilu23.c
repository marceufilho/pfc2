/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu23(long v0, long v1)
{
    REQUIRES(((0 == v0) && (0 == v1)));
    while ((v0 < 100)) {
        INVARIANT((((v0 * 2) == v1) && (v0 <= 100)));
        v1 = (2 + v1);
        v0 = (1 + v0);
    }
    ASSERT((200 == v1));
    return v1;
}
