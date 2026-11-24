/* Hand transcription of examples/01_count/count.c. The loop bounds PFC2 infers are written here. */
/*@ requires 0 <= n;
    terminates \false;
    assigns \nothing;
    ensures \result == n;
*/
long count(long n)
{
    long i = 0;
    /*@ loop invariant 0 <= i <= n;
        loop assigns i;
    */
    while (i < n) {
        i++;
    }
    return i;
}

/*@ requires 0 <= n;
    terminates \false;
    assigns \nothing;
*/
void counting_to_n_gives_n(long n)
{
    long r = count(n);
    /*@ assert r == n; */
}
