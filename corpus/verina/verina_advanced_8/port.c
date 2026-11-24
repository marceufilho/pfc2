#include "pfc.h"

/* Verina verina_advanced_8: smallest station index from which the circuit can be completed, or -1. */
long canCompleteCircuit(long gas_len, const long gas[gas_len], long cost_len, const long cost[cost_len])
    requires(gas_len == cost_len)
    requires(gas_len > 0)
    ensures(result >= -1 && result < gas_len)
{
    long total = 0;
    long tank = 0;
    long start = 0;

    for (long i = 0; i < gas_len; i++) invariant(0 <= i && i <= gas_len && 0 <= start && start <= i && tank >= 0 && (start != i || tank == 0) && total <= tank && (start == 0 || total < tank)) {
        long gain = gas[i] - cost[i];

        total += gain;
        tank += gain;
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }
    if (total < 0) {
        return -1;
    }
    return start;
}
