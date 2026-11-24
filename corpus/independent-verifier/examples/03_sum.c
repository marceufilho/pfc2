/* Hand transcription of examples/03_sum/sum.c. No bound on the elements: the addition is not claimed safe. */
/*@ requires 0 <= n;
    requires \valid_read(a + (0 .. n-1));
    terminates \false;
    assigns \nothing;
*/
long sum(long n, const long a[n])
{
    long s = 0;
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, s;
    */
    for (long i = 0; i < n; i++) {
        s += a[i];
    }
    return s;
}
