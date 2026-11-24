/* Independent ACSL transcription of kernels/sum/kernel.c. */
/*@  requires 0 <= n <= a_len;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    terminates \false;
    assigns \nothing;
*/
long sum(const long a[], long a_len, long n)
{
    long s = 0;
    long i = 0;
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, s;
    */
    while (i < n) {
        /*@ assert bounds_a: 0 <= i < a_len; */
        s = s + a[i];
        i = i + 1;
    }
    return s;
}
