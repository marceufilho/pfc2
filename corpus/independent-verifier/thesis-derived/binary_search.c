/* Independent ACSL transcription; sortedness is unnecessary for bounds safety. */
/*@  requires 0 <= n <= a_len;
    requires a_len > 0 ==> \valid_read(a + (0 .. a_len-1));
    terminates \false;
    assigns \nothing;
*/
long binary_search(const long a[], long a_len, long n, long needle)
{
    long lo = 0;
    long hi = n - 1;
    /*@ loop invariant 0 <= lo && lo <= hi+1 && hi < n;
        loop assigns lo, hi;
    */
    while (lo <= hi) {
        /*@ assert division_mid: 2 != 0 && !((hi-lo) == (-9223372036854775807-1) && 2 == -1); */
        long mid = lo + (hi - lo) / 2;
        /*@ assert bounds_a: 0 <= mid < a_len; */
        long value = a[mid];
        if (value < needle) { lo = mid + 1; }
        else {
            if (needle < value) { hi = mid - 1; }
            else { return mid; }
        }
    }
    return -1;
}
