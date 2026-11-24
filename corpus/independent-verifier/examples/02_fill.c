/* Hand transcription of examples/02_fill/fill.c. */
/*@ requires 0 <= n;
    requires \valid(a + (0 .. n-1));
    terminates \false;
    assigns a[0 .. n-1];
*/
long fill(long n, long a[n], long value)
{
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, a[0 .. n-1];
    */
    for (long i = 0; i < n; i++) {
        a[i] = value;
    }
    return n;
}
