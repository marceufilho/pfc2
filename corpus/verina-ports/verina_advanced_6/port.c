#include "pfc.h"

/* Verina verina_advanced_6: 1 when s contains each of a, e, i, o, u in either case. */
long allVowels(long s_len, const char s[s_len])
{
    long has_a = 0;
    long has_e = 0;
    long has_i = 0;
    long has_o = 0;
    long has_u = 0;

    for (long k = 0; k < s_len; k++) {
        if (s[k] == 'a' || s[k] == 'A') {
            has_a = 1;
        } else if (s[k] == 'e' || s[k] == 'E') {
            has_e = 1;
        } else if (s[k] == 'i' || s[k] == 'I') {
            has_i = 1;
        } else if (s[k] == 'o' || s[k] == 'O') {
            has_o = 1;
        } else if (s[k] == 'u' || s[k] == 'U') {
            has_u = 1;
        }
    }
    if (has_a && has_e && has_i && has_o && has_u) {
        return 1;
    }
    return 0;
}
