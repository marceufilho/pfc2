#include "pfc.h"

/* SV-COMP c/array-fpi/res2o.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long res2o(long N, long sum_len, long sum[sum_len], long a[N], long b[N], long c[N])
    requires(0 < N && N <= 536870911)
    requires(sum_len == 1)
{

    long i = 0;

    sum[0] = 0;
    for(i=0; i<N; i++)
    {
        a[i] = 1;
    }

    for(i=0; i<N; i++)
    {
        b[i] = 1;
    }

    for(i=0; i<N; i++)
    {
        c[i] = 1;
    }

    for(i=0; i<N; i++)
    {
        sum[0] = sum[0] + a[i];
    }

    for(i=0; i<N; i++)
    {
        sum[0] = sum[0] + b[i];
    }

    for(i=0; i<N; i++)
    {
        sum[0] = sum[0] + c[i];
    }

    return 1;
}
