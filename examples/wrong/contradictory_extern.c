#include "pfc.h"

/* No number is both below 0 and above 100, so this contract describes no function. Because a declared
 * function is trusted under its contract, an impossible contract would let anything after the call be
 * "proved". Refused before any proof is accepted. */
long sensor(void)
    ensures(result < 0 && result > 100);

long read_twice(void)
    ensures(result == 7)
{
    return sensor() + sensor();
}
