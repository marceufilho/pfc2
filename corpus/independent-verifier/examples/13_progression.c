/* Hand transcription of examples/13_progression/progression.c. */
/*@ requires -1000 <= start && start <= 1000;
    requires -1000 <= step && step <= 1000;
    requires 0 <= n && n <= 1000;
    terminates \false;
    assigns \nothing;
    ensures \result == start + n * step;
*/
long term(long start, long step, long n)
{
    long value = start;
    /*@ loop invariant 0 <= i <= n;
        loop invariant value == start + i * step;
        loop assigns i, value;
    */
    for (long i = 0; i < n; i++) {
        value += step;
    }
    return value;
}

/*@ requires 0 <= n && n <= 1000;
    terminates \false;
    assigns \nothing;
*/
void counting_is_a_progression(long n)
{
    long r = term(0, 1, n);
    /*@ assert r == n; */
}

/*@ requires -1000 <= start && start <= 1000;
    requires -1000 <= step && step <= 1000;
    requires 0 <= n && n < 1000;
    terminates \false;
    assigns \nothing;
*/
void consecutive_terms_differ_by_the_step(long start, long step, long n)
{
    long next = term(start, step, n + 1);
    long this = term(start, step, n);
    /*@ assert next - this == step; */
}

/*@ requires -1000 <= start && start <= 1000;
    requires -1000 <= step && step <= 1000;
    requires 1 <= n && n < 1000;
    terminates \false;
    assigns \nothing;
*/
void a_term_is_the_average_of_its_neighbours(long start, long step, long n)
{
    long middle = term(start, step, n);
    long before = term(start, step, n - 1);
    long after = term(start, step, n + 1);
    /*@ assert 2 * middle == before + after; */
}

/*@ requires -1000 <= start && start <= 1000;
    requires 0 <= n && n <= 1000;
    terminates \false;
    assigns \nothing;
*/
void a_zero_step_stays_put(long start, long n)
{
    long r = term(start, 0, n);
    /*@ assert r == start; */
}

/*@ requires -100 <= start && start <= 100;
    requires -1 <= step && step <= 1;
    requires 0 <= n && n <= 900;
    terminates \false;
    assigns \nothing;
*/
void stepping_back_returns_to_the_start(long start, long step, long n)
{
    long there = term(start, step, n);
    long back = term(there, 0 - step, n);
    /*@ assert back == start; */
}
