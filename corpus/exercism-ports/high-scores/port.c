#include "pfc.h"

#define MAX_TOP_SCORES 3

/* `int32_t` elements stay `int`; lengths and results become `long` (P1, P4). */
long latest_score(long n, const int scores[n])
{
    if (n == 0) {
        return 0;
    }
    return scores[n - 1];
}

long best_score(long n, const int scores[n])
{
    if (n == 0) {
        return 0;
    }
    long best = scores[0];

    for (long i = 1; i < n; i++) {
        if (best < scores[i]) {
            best = scores[i];
        }
    }
    return best;
}

/* Writes the highest scores to `output`, highest first; returns how many. */
long top_three(long n, const int scores[n], long m, int output[m])
{
    long count = 0;

    for (long i = 0; i < n; i++) {
        long score = scores[i];

        if (count < MAX_TOP_SCORES) {
            count++;
        } else if (score <= output[count - 1]) {
            continue;
        }
        long k = count - 1;

        while (k > 0 && output[k - 1] < score) {
            output[k] = output[k - 1];
            --k;
        }
        output[k] = score;
    }
    return count;
}
