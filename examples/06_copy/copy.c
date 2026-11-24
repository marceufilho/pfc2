#include "pfc.h"

/* Two arrays that do not overlap. The law states what a caller may rely on. */
long copy(long n, long dst[n], const long src[n])
    requires(separated(dst, src))
{
    for (long i = 0; i < n; i++) {
        dst[i] = src[i];
    }
    return n;
}
