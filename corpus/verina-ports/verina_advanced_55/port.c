#include "pfc.h"

/* Verina verina_advanced_55: the most frequent element; among ties, the one that occurs first. */
long mostFrequent(long xs_len, const long xs[xs_len])
{
    long best = 0;
    long best_count = 0;

    for (long i = 0; i < xs_len; i++) {
        long count = 0;

        for (long j = 0; j < xs_len; j++) {
            if (xs[j] == xs[i]) {
                count++;
            }
        }
        if (count > best_count) {
            best = xs[i];
            best_count = count;
        }
    }
    return best;
}
