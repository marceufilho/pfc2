/* Host C: the upstream interface on top of the port. Not verified. */
#include "perfect_numbers.h"

long classify(long n);

kind classify_number(int n)
{
   return (kind)classify(n);
}
