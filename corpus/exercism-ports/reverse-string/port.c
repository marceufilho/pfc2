#include "pfc.h"

/* Writes `value` reversed, with its terminator, to `out`. Upstream allocates the result and walks two
 * pointers; the port receives the buffer (P3) and walks two indices (P11). */
long reverse_into(long n, const char value[n], long m, char out[m])
{
    long dest = n;
    long at = 0;

    out[dest] = '\0';
    while (at < n) {
        --dest;
        out[dest] = value[at];
        ++at;
    }
    return 0;
}
