#include "pfc.h"

/* Verina verina_advanced_75: largest sum of a non-empty contiguous subarray (Kadane's algorithm). */
long task_code(long sequence_len, const long sequence[sequence_len])
    requires(sequence_len >= 1)
{
    long cur = sequence[0];
    long max_so_far = sequence[0];

    for (long i = 1; i < sequence_len; i++) invariant(1 <= i && i <= sequence_len) {
        if (cur + sequence[i] > sequence[i]) {
            cur = cur + sequence[i];
        } else {
            cur = sequence[i];
        }
        if (cur > max_so_far) {
            max_so_far = cur;
        }
    }
    return max_so_far;
}
