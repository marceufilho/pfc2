/* Host C: the upstream interface on top of the port. Not verified. */
#include "nth_prime.h"

long nth_prime(long n);

uint32_t nth(uint32_t n)
{
   return (uint32_t)nth_prime(n);
}
