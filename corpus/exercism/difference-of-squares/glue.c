/* Host C: the upstream interface on top of the port. Not verified. */
#include "difference_of_squares.h"

long squares_sum(long number);
long sum_squared(long number);
long squares_difference(long number);

unsigned int sum_of_squares(unsigned int number)
{
   return (unsigned int)squares_sum(number);
}

unsigned int square_of_sum(unsigned int number)
{
   return (unsigned int)sum_squared(number);
}

unsigned int difference_of_squares(unsigned int number)
{
   return (unsigned int)squares_difference(number);
}
