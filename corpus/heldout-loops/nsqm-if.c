#include "pfc.h"

/* SV-COMP c/array-fpi/nsqm-if.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long nsqm_if(long N, long a[N], long b[N])
    requires(0 < N && N <= 536870911)
{

    long i = 0;

    for(i=0; i<N; i++)
    {
        if(i==0) {
            b[0] = 1;
        } else {
            b[i] = b[i-1] + 2;
        }
    }

    for(i=0; i<N; i++)
    {
        if(i==0) {
            a[0] = N + 1;
        } else {
            a[i] = a[i-1] + b[i-1] + 2;
        }
    }

    for(i=0; i<N; i++)
    {
    }
    return 1;
}
