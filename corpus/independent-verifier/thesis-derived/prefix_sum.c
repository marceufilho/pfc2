/* Independent ACSL transcription of kernels/prefix_sum/kernel.c. */
/*@  requires 0 <= n <= a_len;
    requires a_len > 0 ==> \valid(a + (0 .. a_len-1));
    terminates \false;
    assigns a[0 .. n-1];
*/
long prefix_sum(long a[], long a_len, long n)
{
    if (n == 0) { return 0; }
    long i = 1;
    /*@ loop invariant 1 <= i <= n;
        loop assigns i, a[0 .. n-1];
    */
    while (i < n) {
        /*@ assert bounds_a_read: 0 <= i < a_len; */
        /*@ assert bounds_previous: 0 <= i-1 < a_len; */
        /*@ assert bounds_a_write: 0 <= i < a_len; */
        a[i] = a[i] + a[i - 1];
        i = i + 1;
    }
    return n;
}
