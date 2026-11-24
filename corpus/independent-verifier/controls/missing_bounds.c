/* n <= a_len deliberately absent; allocation validity remains. */
/*@  requires 0 <= n && 0 <= a_len;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    terminates \false;
    assigns \nothing;
*/
long missing_bounds(const long a[], long a_len, long n)
{
    long i = 0;
    long s = 0;
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
