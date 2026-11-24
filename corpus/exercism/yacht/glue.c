/* Host C: the upstream interface on top of the port. Not verified. */
#include "yacht.h"

long yacht_score(long n, const int faces[], long category);

int score(dice_t dice, category_t category)
{
   return (int)yacht_score(5, dice.faces, (long)(int)category);
}
