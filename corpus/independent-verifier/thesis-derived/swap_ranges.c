/* Independently annotated safety port; upstream attribution: bench/external/acsl/LICENSE. */
/*@  requires 0 <= n <= a_len && n <= b_len;
    requires a_len > 0 ==> \valid(a + (0 .. a_len-1));
    requires b_len > 0 ==> \valid(b + (0 .. b_len-1));
    requires \separated(a + (0 .. a_len-1), b + (0 .. b_len-1));
    terminates \false;
    assigns a[0 .. n-1], b[0 .. n-1];
*/
long swap_ranges(long a[], long a_len, long b[], long b_len, long n)
{
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, a[0 .. n-1], b[0 .. n-1];
    */
    for (long i = 0; i < n; i = i + 1) {
        /*@ assert bounds_a_read: 0 <= i < a_len; */
        long saved = a[i];
        /*@ assert bounds_b_read: 0 <= i < b_len; */
        /*@ assert bounds_a_write: 0 <= i < a_len; */
        a[i] = b[i];
        /*@ assert bounds_b_write: 0 <= i < b_len; */
        b[i] = saved;
    }
    return n;
}
