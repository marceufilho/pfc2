/* Independently annotated safety port; upstream attribution: bench/external/acsl/LICENSE. */
/*@  requires 0 <= n <= a_len;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    terminates \false;
    assigns \nothing;
*/
long count(const long a[], long a_len, long n, long v)
{
    long counted = 0;
    /*@ loop invariant 0 <= counted <= i <= n;
        loop assigns i, counted;
    */
    for (long i = 0; i < n; i = i + 1) {
        /*@ assert bounds_a: 0 <= i < a_len; */
        if (a[i] == v) { counted = counted + 1; }
    }
    return counted;
}
