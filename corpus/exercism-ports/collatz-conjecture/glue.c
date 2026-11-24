/* Host C: the upstream interface on top of the port. Not verified. */
#include "collatz_conjecture.h"

long collatz_steps(long start);

int steps(int start)
{
   return (int)collatz_steps(start);
}
