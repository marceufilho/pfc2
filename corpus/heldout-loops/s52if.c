#include "pfc.h"

/* SV-COMP c/array-fpi/s52if.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long s52if(long N, long sum_len, long sum[sum_len], long a[N])
    requires(0 < N && N <= 357913941)
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
        if(a[i] == 1) {
            a[i] = a[i] + 5;
        } else {
            a[i] = a[i] - 1;
        }
    }

    for(i=0; i<N; i++)
    {
        if(a[i] == 6)
        {
            sum[0] = sum[0] + a[i];
        } else {
            sum[0] = sum[0] * a[i];
        }
    }

    return 1;
}
