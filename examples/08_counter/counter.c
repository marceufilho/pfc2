#include "pfc.h"

/* Globals are part of the state. A caller keeps what it knows about the globals a function does
 * not write, and learns about the others only what the function's `ensures` says. */
long hits = 0;
long limit = 100;

long hit(void)
    requires(0 <= hits)
    ensures(0 <= hits)
    ensures(result == hits)
{
    if (hits < limit) {
        hits++;
    }
    return hits;
}

long twice(void)
    requires(0 <= hits)
{
    long before = limit;

    hit();
    hit();
    assert(limit == before);
    return hits;
}
