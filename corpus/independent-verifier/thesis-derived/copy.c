/* Independently annotated safety port; upstream attribution: bench/external/acsl/LICENSE. */
/*@  requires 0 <= n <= a_len && n <= b_len;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    requires b_len > 0 ==> \valid(b + (0 .. b_len-1));
    requires \separated(a + (0 .. a_len-1), b + (0 .. b_len-1));
    terminates \false;
    assigns b[0 .. n-1];
*/
long copy(const long a[], long a_len, long b[], long b_len, long n)
{
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, b[0 .. n-1];
    */
    for (long i = 0; i < n; i = i + 1) {
        /*@ assert bounds_a: 0 <= i < a_len; */
        /*@ assert bounds_b: 0 <= i < b_len; */
        b[i] = a[i];
    }
    return n;
}
