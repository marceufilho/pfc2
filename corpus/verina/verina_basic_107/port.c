#include "pfc.h"

/* Verina verina_basic_107: the average of a and b by integer division. */
long ComputeAvg(long a, long b)
    ensures(((a + b) % 2 >= 0 && 2 * result == a + b - (a + b) % 2) || ((a + b) % 2 < 0 && 2 * result == a + b - ((a + b) % 2 + 2)))
{
    return (a + b) / 2;
}
