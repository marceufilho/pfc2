#include "pfc.h"

/* The smallest proved program. Nothing is written for the loop: its bounds 0 <= i <= n are
 * proposed from its shape and kept because the checker proves them. */
long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;

    while (i < n) {
        i++;
    }
    return i;
}

/* A law is proved for every input; it is never run. This one covers every n a long can hold. */
law counting_to_n_gives_n(long n where(0 <= n))
{
    assert(count(n) == n);
}
