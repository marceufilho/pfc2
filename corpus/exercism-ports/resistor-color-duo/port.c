#include "pfc.h"

/* The enum values arrive as `int` elements (P5). */
long duo_code(long n, const int colors[n])
{
    return (colors[0] * 10 + colors[1]);
}
