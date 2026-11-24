/* Host C: the upstream interface on top of the port. Not verified. */
#include "pangram.h"
#include <stddef.h>
#include <string.h>

_Bool pangram(long n, const char sentence[]);

bool is_pangram(const char *sentence)
{
   static const char empty[1] = "";
   if (sentence == NULL) {
      return pangram(0, empty);
   }
   return pangram((long)strlen(sentence), sentence);
}
