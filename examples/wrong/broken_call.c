#include "pfc.h"

long half(long x)
    requires(0 <= x)
{
    return x / 2;
}

/* The caller passes a value the callee's contract forbids. Refused at line 12. */
long use(void)
{
    return half(-4);
}
