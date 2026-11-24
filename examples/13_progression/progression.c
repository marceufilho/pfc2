#include "pfc.h"

/* The n-th term of an arithmetic progression, computed the slow way: begin at `start` and add `step`
 * n times. The contract says what that loop amounts to: start + n * step. */
long term(long start, long step, long n)
    requires(-1000 <= start && start <= 1000)
    requires(-1000 <= step && step <= 1000)
    requires(0 <= n && n <= 1000)
    ensures(result == start + n * step)
{
    long value = start;

    for (long i = 0; i < n; i++) invariant(value == start + i * step) {
        value += step;
    }
    return value;
}

/* A test would check a few cases: term(0, 1, 5) == 5, term(2, 3, 4) == 14, term(7, 0, 9) == 7.
 * Each law below is proved for every start, step and n in the ranges: about four billion cases each. */

/* Counting is the progression that starts at 0 and steps by 1. */
law counting_is_a_progression(long n where(0 <= n && n <= 1000))
{
    assert(term(0, 1, n) == n);
}

/* Two consecutive terms differ by exactly the step, wherever you are in the progression. */
law consecutive_terms_differ_by_the_step(
    long start where(-1000 <= start && start <= 1000),
    long step where(-1000 <= step && step <= 1000),
    long n where(0 <= n && n < 1000))
{
    assert(term(start, step, n + 1) - term(start, step, n) == step);
}

/* Every term is the average of its two neighbours. */
law a_term_is_the_average_of_its_neighbours(
    long start where(-1000 <= start && start <= 1000),
    long step where(-1000 <= step && step <= 1000),
    long n where(1 <= n && n < 1000))
{
    assert(2 * term(start, step, n) == term(start, step, n - 1) + term(start, step, n + 1));
}

/* With a step of zero the progression never moves. */
law a_zero_step_stays_put(long start where(-1000 <= start && start <= 1000), long n where(0 <= n && n <= 1000))
{
    assert(term(start, 0, n) == start);
}

/* Reversing the step walks back to where you began. The ranges are narrower here because the first
 * result is passed on as a start, which `term` only accepts between -1000 and 1000: the checker refused
 * a wider version of this law and showed start = 47, step = 1, n = 960. */
law stepping_back_returns_to_the_start(
    long start where(-100 <= start && start <= 100),
    long step where(-1 <= step && step <= 1),
    long n where(0 <= n && n <= 900))
{
    assert(term(term(start, step, n), 0 - step, n) == start);
}
