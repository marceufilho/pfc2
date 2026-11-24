#include "pfc.h"

/* Verina verina_advanced_5: add two numbers given as digit lists, least significant digit first; the digits of
 * the sum go to out in the same order and their count is returned. */
long addTwoNumbers(long l1_len, const long l1[l1_len], long l2_len, const long l2[l2_len], long out_cap, long out[out_cap])
    requires(out_cap > l1_len && out_cap > l2_len)
{
    long i = 0;
    long carry = 0;

    while (i < l1_len || i < l2_len || carry > 0) {
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
