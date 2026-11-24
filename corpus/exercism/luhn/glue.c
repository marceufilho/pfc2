/* Host C: the upstream interface on top of the port. Not verified. */
#include "luhn.h"
#include <stddef.h>
#include <string.h>

_Bool luhn_valid(long n, const char num[]);

bool luhn(const char *num)
{
   if (num == NULL) {
      return false;
   }
   return luhn_valid((long)strlen(num), num);
}
