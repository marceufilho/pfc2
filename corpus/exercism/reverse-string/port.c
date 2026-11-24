#include "pfc.h"

/* Writes `value` reversed, with its terminator, to `out`. Upstream allocates the result and walks two
 * pointers; the port receives the buffer (P3) and walks two indices (P11). */
long reverse_into(long n, const char value[n], long m, char out[m])
    requires(n < m && separated(out, value))
    ensures(out[n] == '\0')
    ensures(n == 0 || (out[0] == value[n - 1] && out[n - 1] == value[0]))
{
    long dest = n;
    long at = 0;

    out[dest] = '\0';
    while (at < n) invariant(0 <= at && at <= n && dest == n - at && out[n] == '\0' && (at == 0 || (out[n - 1] == value[0] && out[dest] == value[at - 1]))) {
        --dest;
        out[dest] = value[at];
        ++at;
    }
    return 0;
}
