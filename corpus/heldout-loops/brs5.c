#include "pfc.h"

/* SV-COMP c/array-fpi/brs5.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long brs5(long N, long sum_len, long sum[sum_len], long a[N])
    requires(0 < N && N <= 429496729)
    requires(sum_len == 1)
{

    long i = 0;

    for(i=0; i<N; i++)
    {
        if(i%5==0) {
            a[i] = 5;
        } else {
            a[i] = 0;
        }
    }

    for(i=0; i<N; i++)
    {
        if(i==0) {
            sum[0] = 0;
        } else {
            sum[0] = sum[0] + a[i];
        }
    }
    return 1;
}
