#include "pfc.h"

#define MAX_TOP_SCORES 3

/* `int32_t` elements stay `int`; lengths and results become `long` (P1, P4). */
long latest_score(long n, const int scores[n])
    ensures(n != 0 || result == 0)
    ensures(n == 0 || result == scores[n - 1])
{
    if (n == 0) {
        return 0;
    }
    return scores[n - 1];
}

long best_score(long n, const int scores[n])
    ensures(n != 0 || result == 0)
    ensures(n == 0 || (result >= scores[0] && result >= scores[n - 1]))
{
    if (n == 0) {
        return 0;
    }
    long best = scores[0];

    for (long i = 1; i < n; i++) invariant(1 <= i && i <= n && best >= scores[0] && best >= scores[i - 1]) {
        if (best < scores[i]) {
            best = scores[i];
        }
    }
    return best;
}

/* Writes the highest scores to `output`, highest first; returns how many. */
long top_three(long n, const int scores[n], long m, int output[m])
    requires(MAX_TOP_SCORES <= m && separated(output, scores))
    ensures((n <= MAX_TOP_SCORES && result == n) || (n > MAX_TOP_SCORES && result == MAX_TOP_SCORES))
    ensures(result < 2 || output[0] >= output[1])
    ensures(result < 3 || output[1] >= output[2])
{
    long count = 0;

    for (long i = 0; i < n; i++) invariant(0 <= i && i <= n && ((i <= 3 && count == i) || (i > 3 && count == 3)) && (count < 2 || output[0] >= output[1]) && (count < 3 || output[1] >= output[2])) {
        long score = scores[i];

        if (count < MAX_TOP_SCORES) {
            count++;
        } else if (score <= output[count - 1]) {
            continue;
        }
        long k = count - 1;

        while (k > 0 && output[k - 1] < score) invariant(0 <= k && k < count && count <= 3 && (k != 2 || output[0] >= output[1]) && (k != 1 || count < 3 || (output[0] >= output[2] && output[2] < score)) && (k != 0 || count < 2 || output[1] < score) && (k != 0 || count < 3 || output[1] >= output[2])) {
            output[k] = output[k - 1];
            --k;
        }
        output[k] = score;
    }
    return count;
}
