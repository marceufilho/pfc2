#include "pfc.h"

/* Adding at most 1000 small steps cannot overflow. The invariant says how the total grows; with it
 * the file certifies at the default --level full: no runtime check of any kind remains. */
long bounded_sum(long n, long step)
    requires(0 <= n && n <= 1000)
    requires(0 <= step && step <= 1000)
    ensures(result == n * step)
{
    long total = 0;

    for (long i = 0; i < n; i++) invariant(total == i * step) {
        total += step;
    }
    return total;
}

/* Each law is proved for every n and step from 0 to 1000: about a million cases each. */

/* One more step adds exactly one step. */
law one_more_step_adds_the_step(long n where(0 <= n && n < 1000), long step where(0 <= step && step <= 1000))
{
    assert(bounded_sum(n + 1, step) == bounded_sum(n, step) + step);
}

/* n steps of size s reach the same place as s steps of size n. */
law the_count_and_the_step_can_be_swapped(long n where(0 <= n && n <= 1000), long step where(0 <= step && step <= 1000))
{
    assert(bounded_sum(n, step) == bounded_sum(step, n));
}
