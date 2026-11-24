/* Hand transcription of examples/06_copy/copy.c. */
/*@ requires 0 <= n;
    requires \valid(dst + (0 .. n-1));
    requires \valid_read(src + (0 .. n-1));
    requires \separated(dst + (0 .. n-1), src + (0 .. n-1));
    terminates \false;
    assigns dst[0 .. n-1];
*/
long copy(long n, long dst[n], const long src[n])
{
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, dst[0 .. n-1];
    */
    for (long i = 0; i < n; i++) {
        dst[i] = src[i];
    }
    return n;
}
