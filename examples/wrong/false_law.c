#include "pfc.h"

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

/* Refused: counting to n never gives n + 1, and the checker shows a value at line 18. */
law counting_to_n_gives_one_more(long n where(0 <= n))
{
    assert(count(n) == n + 1);
}
