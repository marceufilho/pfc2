/* Host C: the upstream interface on top of the port. Not verified. */
#include "reverse_string.h"
#include <stdlib.h>
#include <string.h>

long reverse_into(long n, const char value[], long m, char out[]);

char *reverse(const char *value)
{
   size_t n = strlen(value);
   char *out = malloc(n + 1);
   if (out == NULL) {
      return NULL;
   }
   reverse_into((long)n, value, (long)n + 1, out);
   return out;
}
