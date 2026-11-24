#include "pfc.h"

/* Verina verina_advanced_71: the shortest non-empty substring of s with exactly k characters '1'; among those
 * of that length the lexicographically smallest; written to out, its length returned (0 when there is none). */
long shortestBeautifulSubstring(long s_len, const char s[s_len], long k, long out_cap, char out[out_cap])
    requires(out_cap >= s_len)
    requires(0 <= s_len)
    requires(0 <= k)
    /* Consequence of the dropped "result is one of the substrings of s". */
    ensures(0 <= result && result <= s_len)
{
    long best_start = 0;
    long best_len = 0;

    for (long i = 0; i < s_len; i++) invariant(0 <= i && i <= s_len && 0 <= best_start && 0 <= best_len && best_start + best_len <= s_len) {
        long ones = 0;

        for (long j = i; j < s_len; j++) invariant(i <= j && j <= s_len && 0 <= ones && ones <= j - i && 0 <= best_start && 0 <= best_len && best_start + best_len <= s_len) {
            if (s[j] == '1') {
                ones++;
            }
            if (ones > k) {
                break;
            }
            if (ones == k) {
                long len = j - i + 1;
                long better = 0;

                if (best_len == 0 || len < best_len) {
                    better = 1;
                } else if (len == best_len) {
                    for (long t = 0; t < len; t++) invariant(0 <= t && t <= len) {
                        if (s[i + t] != s[best_start + t]) {
                            if (s[i + t] < s[best_start + t]) {
                                better = 1;
                            }
                            break;
                        }
                    }
                }
                if (better) {
                    best_start = i;
                    best_len = len;
                }
                break;
            }
        }
    }
    for (long t = 0; t < best_len; t++) invariant(0 <= t && t <= best_len) decreases(best_len - t) {
        out[t] = s[best_start + t];
    }
    return best_len;
}
