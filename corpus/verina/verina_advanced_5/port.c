#include "pfc.h"

/* Verina verina_advanced_5: add two numbers given as digit lists, least significant digit first; the digits of
 * the sum go to out in the same order and their count is returned. */
long addTwoNumbers(long l1_len, const long l1[l1_len], long l2_len, const long l2[l2_len], long out_cap, long out[out_cap])
    requires(out_cap > l1_len && out_cap > l2_len)
    requires(l1_len > 0 && l2_len > 0)
    requires(l1[l1_len - 1] != 0 || l1_len == 1)
    requires(l2[l2_len - 1] != 0 || l2_len == 1)
    ensures(result >= 1)
    ensures(out[result - 1] != 0 || (l1_len == 1 && l1[0] == 0 && l2_len == 1 && l2[0] == 0 && result == 1 && out[0] == 0))
{
    long i = 0;
    long carry = 0;

    while (i < l1_len || i < l2_len || carry > 0) invariant(0 <= i && 0 <= carry) {
        long sum = carry;

        if (i < l1_len) {
            sum += l1[i];
        }
        if (i < l2_len) {
            sum += l2[i];
        }
        out[i] = sum % 10;
        carry = sum / 10;
        i++;
    }
    return i;
}
