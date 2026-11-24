#include "pfc.h"

/* SV-COMP c/loop-invgen/id_build.i, ported by rules H1, H4, H5, H8. */
long id_build(long nlen)
{
    long offset = 0;
    long length = 0;
    long i = 0;
    long j = 0;
    for (i = 0; i < nlen; i++) {
        for (j = 0; j < 8; j++) {
            assert(0 <= nlen - 1 - i);
            assert(nlen - 1 - i < nlen);
        }
    }
    return 0;
}
