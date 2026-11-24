/* Independently annotated safety port; upstream attribution: bench/external/acsl/LICENSE. */
/*@  requires 0 <= n <= a_len;
    requires a_len > 0 ==> \valid(a + (0 .. a_len-1));
    terminates \false;
    assigns a[0 .. n-1];
*/
long replace(long a[], long a_len, long n, long v, long w)
{
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, a[0 .. n-1];
    */
    for (long i = 0; i < n; i = i + 1) {
        /*@ assert bounds_a_read: 0 <= i < a_len; */
        if (a[i] == v) {
            /*@ assert bounds_a_write: 0 <= i < a_len; */
            a[i] = w;
        }
    }
    return n;
}
