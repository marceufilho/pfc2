#include "pfc.h"

long saxpy(long alpha, const long x[], long x_len, long y[], long y_len, long n)
{
    REQUIRES(0 <= n && n <= x_len && n <= y_len);
    REQUIRES(SEPARATED(x, x_len, y, y_len));
    long i = 0;
    while (i < n) {
        INVARIANT(0 <= i && i <= n);
        y[i] = alpha * x[i] + y[i];
        i = i + 1;
    }
    return n;
}
