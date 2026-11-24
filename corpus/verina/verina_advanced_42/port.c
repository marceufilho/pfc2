#include "pfc.h"

/* Verina verina_advanced_42: the best profit of buying on one day and selling on a later one, or 0. */
long maxProfit(long prices_len, const long prices[prices_len])
    requires(prices_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= prices_len */
    /* Of result = 0 <-> (length <= 1 or no profitable pair), the direction length <= 1 -> result = 0 is
     * stated; everything quantified over index pairs is dropped. result is a Nat. Prices are Nats in
     * Verina; that needs a quantifier over the elements and is not assumed here. */
    ensures(prices_len > 1 || result == 0)
    ensures(result >= 0)
{
    if (prices_len == 0) {
        return 0;
    }
    long lowest = prices[0];
    long best = 0;

    for (long i = 1; i < prices_len; i++) invariant(best >= 0 && (prices_len > 1 || best == 0)) {
        if (prices[i] - lowest > best) {
            best = prices[i] - lowest;
        }
        if (prices[i] < lowest) {
            lowest = prices[i];
        }
    }
    return best;
}
