/* Valid implications must not hide the inconsistent requirements. */
/*@  requires n < 0 && n > 0;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    terminates \false;
    assigns \nothing;
*/
long vacuous(const long a[], long a_len, long n)
{
    /*@ assert bounds_a: 0 <= n < a_len; */
    return a[n];
}
