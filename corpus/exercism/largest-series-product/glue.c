/* Host C: the upstream interface on top of the port. Not verified. */
#include "largest_series_product.h"
#include <limits.h>
#include <string.h>

long largest_product_of(long n, const char digits[], long span);

int64_t largest_series_product(char *digits, size_t span)
{
   /* A span that does not fit a long (the upstream test passes -1, which is SIZE_MAX) saturates. */
   long wide = span > (size_t)LONG_MAX ? LONG_MAX : (long)span;
   return largest_product_of((long)strlen(digits), digits, wide);
}
