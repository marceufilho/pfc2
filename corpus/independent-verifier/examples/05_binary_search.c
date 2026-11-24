/* Hand transcription of examples/05_binary_search/binary_search.c. */
/*@ requires 0 <= n;
    requires \valid_read(a + (0 .. n-1));
    terminates \false;
    assigns \nothing;
    ensures -1 <= \result && \result < n;
    ensures \result == -1 || a[\result] == key;
*/
long binary_search(long n, const long a[n], long key)
{
    long lo = 0;
    long hi = n;

    /*@ loop invariant 0 <= lo && lo <= hi && hi <= n;
        loop assigns lo, hi;
        loop variant hi - lo;
    */
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;

        if (a[mid] == key) {
            return mid;
        }
        if (a[mid] < key) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return -1;
}

/*@ requires 0 <= n;
    requires \valid_read(a + (0 .. n-1));
    terminates \false;
    assigns \nothing;
*/
void a_found_index_holds_the_key(long n, const long a[n], long key)
{
    long found = binary_search(n, a, key);
    /*@ assert found == -1 || (0 <= found && found < n && a[found] == key); */
}
