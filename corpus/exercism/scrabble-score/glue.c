/* Host C: the upstream interface on top of the port. Not verified. */
#include "scrabble_score.h"
#include <string.h>

long word_score_of(long n, const char word[]);

unsigned int score(const char *word)
{
   return (unsigned int)word_score_of((long)strlen(word), word);
}
