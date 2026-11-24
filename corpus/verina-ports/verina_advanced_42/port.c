#include "pfc.h"

/* Verina verina_advanced_42: the best profit of buying on one day and selling on a later one, or 0. */
long maxProfit(long prices_len, const long prices[prices_len])
{
    if (prices_len == 0) {
        return 0;
    }
    long lowest = prices[0];
    long best = 0;

    for (long i = 1; i < prices_len; i++) {
        if (prices[i] - lowest > best) {
            best = prices[i] - lowest;
        }
        if (prices[i] < lowest) {
            lowest = prices[i];
        }
    }
    return best;
}
