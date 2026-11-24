/* Independent ACSL transcription of kernels/dot/kernel.c. */
/*@  requires 0 <= n <= a_len && n <= b_len;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    requires b_len > 0 ==> \valid_read(b + (0 .. b_len-1));
    terminates \false;
    assigns \nothing;
*/
long dot(const long a[], long a_len, const long b[], long b_len, long n)
{
    long s = 0;
    long i = 0;
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, s;
    */
    while (i < n) {
        /*@ assert bounds_a: 0 <= i < a_len; */
        /*@ assert bounds_b: 0 <= i < b_len; */
        s = s + a[i] * b[i];
        i = i + 1;
    }
    return s;
}
