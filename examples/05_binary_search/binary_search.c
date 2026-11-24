#include "pfc.h"

/* The classic midpoint, written so it cannot overflow. The proof shows every probe is inside the
 * array and that the search stops; it says nothing about the array being sorted. */
long binary_search(long n, const long a[n], long key)
    requires(0 <= n)
    ensures(-1 <= result && result < n)
    ensures(result == -1 || a[result] == key)
{
    long lo = 0;
    long hi = n;

    while (lo < hi) invariant(0 <= lo && lo <= hi && hi <= n) decreases(hi - lo) {
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

/* Whatever the array holds and whatever is searched for: an answer other than -1 is an index of the
 * array, and the key is there. (That -1 means "absent" would need "the array is sorted" and "no element
 * equals the key", both statements about every element, which PFC2 cannot write.) */
law a_found_index_holds_the_key(long n where(0 <= n), const long a[n], long key)
{
    long found = binary_search(n, a, key);

    assert(found == -1 || (0 <= found && found < n && a[found] == key));
}
