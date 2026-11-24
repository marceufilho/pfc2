/* Host C: the upstream interface on top of the port. Not verified. */
#include "high_scores.h"

long latest_score(long n, const int scores[]);
long best_score(long n, const int scores[]);
long top_three(long n, const int scores[], long m, int output[]);

int32_t latest(const int32_t *scores, size_t scores_len)
{
   return (int32_t)latest_score((long)scores_len, scores);
}

int32_t personal_best(const int32_t *scores, size_t scores_len)
{
   return (int32_t)best_score((long)scores_len, scores);
}

size_t personal_top_three(const int32_t *scores, size_t scores_len, int32_t *output)
{
   return (size_t)top_three((long)scores_len, scores, 3, output);
}
