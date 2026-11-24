/* Hand transcription of examples/04_bounded_sum/bounded_sum.c. */
/*@ requires 0 <= n && n <= 1000;
    requires 0 <= step && step <= 1000;
    terminates \false;
    assigns \nothing;
    ensures \result == n * step;
*/
long bounded_sum(long n, long step)
{
    long total = 0;
    /*@ loop invariant 0 <= i <= n;
        loop invariant total == i * step;
        loop assigns i, total;
    */
    for (long i = 0; i < n; i++) {
        total += step;
    }
    return total;
}

/*@ requires 0 <= n && n < 1000;
    requires 0 <= step && step <= 1000;
    terminates \false;
    assigns \nothing;
*/
void one_more_step_adds_the_step(long n, long step)
{
    long more = bounded_sum(n + 1, step);
    long base = bounded_sum(n, step);
    /*@ assert more == base + step; */
}

/*@ requires 0 <= n && n <= 1000;
    requires 0 <= step && step <= 1000;
    terminates \false;
    assigns \nothing;
*/
void the_count_and_the_step_can_be_swapped(long n, long step)
{
    long one = bounded_sum(n, step);
    long other = bounded_sum(step, n);
    /*@ assert one == other; */
}
