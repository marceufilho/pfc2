#include "pfc.h"

/* SV-COMP c/array-fpi/indp5.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long indp5(long N, long a[N], long sum_len, long sum[sum_len])
    requires(0 < N && N <= 536870911)
    requires(sum_len == 1)
{

    long i = 0;

    sum[0] = 0;
    for(i=0;i<N;i++)
    {
        a[i]=((i+1)*(i+1));
    }

    for(i=0;i<N;i++)
    {
        a[i]=a[i]-(i*i);
    }

    for(i=0;i<N;i++)
    {
        a[i]=a[i]-i;
    }

    for(i=0;i<N;i++)
    {
        a[i]=a[i]-i;
    }

    for(i=0;i<N;i++)
    {
        sum[0] = sum[0] + a[i];
    }

    return 1;
}
