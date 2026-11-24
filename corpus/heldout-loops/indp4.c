#include "pfc.h"

/* SV-COMP c/array-fpi/indp4.c, ported by rules H1, H2, H3, H5, H6, H7, H8. */
long indp4(long N, long a[N])
    requires(0 < N && N <= 536870911)
{

    long i = 0;

    for(i=0;i<N;i++)
    {
        a[i]=((i+1)*(i+1));
    }

    for(i=0;i<N;i++)
    {
        a[i]=a[i] - i;
    }

    for(i=0;i<N;i++)
    {
        a[i]=a[i] - i;
    }

    for(i=0;i<N;i++)
    {
    }

    return 1;
}
