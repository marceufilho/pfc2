/* Host C: the upstream interface on top of the port. Not verified. */
#include "sum_of_multiples.h"
#include <stdlib.h>

long multiples_sum(long n, const long factors[], long limit);

unsigned int sum(const unsigned int *factors, const size_t number_of_factors, const unsigned int limit)
{
   if (factors == NULL) {
      return 0;
   }
   long *wide = calloc(number_of_factors + 1, sizeof(long));
   if (wide == NULL) {
      return 0;
   }
   for (size_t i = 0; i < number_of_factors; i++) {
      wide[i] = factors[i];
   }
   unsigned int total = (unsigned int)multiples_sum((long)number_of_factors, wide, limit);
   free(wide);
   return total;
}
