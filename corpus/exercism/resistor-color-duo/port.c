#include "pfc.h"

/* The enum values arrive as `int` elements (P5). */
long duo_code(long n, const int colors[n])
    requires(2 <= n && 0 <= colors[0] && colors[0] <= 9 && 0 <= colors[1] && colors[1] <= 9)
    ensures(result == colors[0] * 10 + colors[1])
{
    return (colors[0] * 10 + colors[1]);
}
