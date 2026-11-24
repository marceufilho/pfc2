/* Independently annotated safety port; upstream attribution: bench/external/acsl/LICENSE. */
/*@  requires 0 <= n <= a_len;
    requires a_len > 0 ==> \valid(a + (0 .. a_len-1));
    terminates \false;
    assigns a[0 .. n-1];
*/
long reverse(long a[], long a_len, long n)
{
    /*@ assert division_half: 2 != 0 && !(n == (-9223372036854775807-1) && 2 == -1); */
    long half = n / 2;
    /*@ loop invariant 0 <= i <= half && half <= n-i;
        loop assigns i, a[0 .. n-1];
    */
    for (long i = 0; i < half; i = i + 1) {
        /*@ assert bounds_left_read: 0 <= i < a_len; */
        long saved = a[i];
        /*@ assert bounds_right_read: 0 <= n-1-i < a_len; */
        /*@ assert bounds_left_write: 0 <= i < a_len; */
        a[i] = a[n - 1 - i];
        /*@ assert bounds_right_write: 0 <= n-1-i < a_len; */
        a[n - 1 - i] = saved;
    }
    return n;
}
