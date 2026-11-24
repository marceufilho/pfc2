/* Independent ACSL transcription of kernels/saxpy/kernel.c. */
/*@  requires 0 <= n <= x_len && n <= y_len;
    requires x_len > 0 ==> \valid_read(x + (0 .. x_len-1));
    requires y_len > 0 ==> \valid(y + (0 .. y_len-1));
    requires \separated(x + (0 .. x_len-1), y + (0 .. y_len-1));
    terminates \false;
    assigns y[0 .. n-1];
*/
long saxpy(long alpha, const long x[], long x_len, long y[], long y_len, long n)
{
    long i = 0;
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, y[0 .. n-1];
    */
    while (i < n) {
        /*@ assert bounds_x_read: 0 <= i < x_len; */
        /*@ assert bounds_y_read: 0 <= i < y_len; */
        /*@ assert bounds_y_write: 0 <= i < y_len; */
        y[i] = alpha * x[i] + y[i];
        i = i + 1;
    }
    return n;
}
