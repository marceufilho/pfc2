#include "pfc.h"

/* SV-COMP c/array-fpi/sina4.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long sina4(long N, long sum_len, long sum[sum_len], long a[N], long b[N])
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
        sum[0] = sum[0] + a[i];
    }

    for(i=0; i<N; i++)
    {
        a[i] = a[i] + sum[0];
    }

    for(i=0; i<N; i++)
    {
        b[i] = a[i] + 1;
    }

    for(i=0; i<N; i++)
    {
    }
    return 1;
}
