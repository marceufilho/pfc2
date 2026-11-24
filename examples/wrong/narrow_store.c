#include "pfc.h"

/* Wrong: a shifted letter may not fit a char ('z' + 13 is 135, and a char holds at most 127 here). */
long shift(long n, char s[n])
    requires(1 <= n && 'a' <= s[0] && s[0] <= 'z')
{
    s[0] = s[0] + 13;
    return 0;
}
