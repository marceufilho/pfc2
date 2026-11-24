/* Host C: the upstream interface on top of the port. Not verified. */
#include "leap.h"

_Bool is_leap_year(long year);

bool leap_year(int year)
{
   return is_leap_year(year);
}
