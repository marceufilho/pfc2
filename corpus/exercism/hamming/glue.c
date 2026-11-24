/* Host C: the upstream interface on top of the port. Not verified. */
#include "hamming.h"
#include <stddef.h>
#include <string.h>

long hamming_distance(long n, const char lhs[], long m, const char rhs[]);

int compute(const char *lhs, const char *rhs)
{
   if (lhs == NULL || rhs == NULL) {
      return -1;
   }
   return (int)hamming_distance((long)strlen(lhs), lhs, (long)strlen(rhs), rhs);
}
