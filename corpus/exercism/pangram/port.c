#include "pfc.h"

#define NUMBER_OF_LETTERS 26

/* tolower and isalpha of the C locale, written out (P7). */
long to_lower(long c)
    ensures((c >= 'A' && c <= 'Z' && result == c + ('a' - 'A')) || (!(c >= 'A' && c <= 'Z') && result == c))
{
    if (c >= 'A' && c <= 'Z') {
        return c + ('a' - 'A');
    }
    return c;
}

_Bool is_alpha(long c)
    ensures(result == ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')))
{
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

/* Does the sentence use every letter. The string arrives with its length (P2); upstream's memset of the
 * table is its initial value (P7); the element is read into a local before the call (P13). */
_Bool pangram(long n, const char sentence[n])
    ensures(n >= NUMBER_OF_LETTERS || !result)
{
    long sentence_length = n;
    _Bool found_letters[NUMBER_OF_LETTERS] = {0};

    for (long i = 0; i < sentence_length; i++) invariant(0 <= i && i <= n && found_letters[0] + found_letters[1] + found_letters[2] + found_letters[3] + found_letters[4] + found_letters[5] + found_letters[6] + found_letters[7] + found_letters[8] + found_letters[9] + found_letters[10] + found_letters[11] + found_letters[12] + found_letters[13] + found_letters[14] + found_letters[15] + found_letters[16] + found_letters[17] + found_letters[18] + found_letters[19] + found_letters[20] + found_letters[21] + found_letters[22] + found_letters[23] + found_letters[24] + found_letters[25] <= i) {
        long current = sentence[i];
        long letter = to_lower(current);

        if (is_alpha(letter)) {
            found_letters[letter - 'a'] = 1;
        }
    }
    for (long i = 0; i < NUMBER_OF_LETTERS; i++) invariant(0 <= i && i <= 26 && found_letters[0] + found_letters[1] + found_letters[2] + found_letters[3] + found_letters[4] + found_letters[5] + found_letters[6] + found_letters[7] + found_letters[8] + found_letters[9] + found_letters[10] + found_letters[11] + found_letters[12] + found_letters[13] + found_letters[14] + found_letters[15] + found_letters[16] + found_letters[17] + found_letters[18] + found_letters[19] + found_letters[20] + found_letters[21] + found_letters[22] + found_letters[23] + found_letters[24] + found_letters[25] <= n && (i <= 0 || found_letters[0]) && (i <= 1 || found_letters[1]) && (i <= 2 || found_letters[2]) && (i <= 3 || found_letters[3]) && (i <= 4 || found_letters[4]) && (i <= 5 || found_letters[5]) && (i <= 6 || found_letters[6]) && (i <= 7 || found_letters[7]) && (i <= 8 || found_letters[8]) && (i <= 9 || found_letters[9]) && (i <= 10 || found_letters[10]) && (i <= 11 || found_letters[11]) && (i <= 12 || found_letters[12]) && (i <= 13 || found_letters[13]) && (i <= 14 || found_letters[14]) && (i <= 15 || found_letters[15]) && (i <= 16 || found_letters[16]) && (i <= 17 || found_letters[17]) && (i <= 18 || found_letters[18]) && (i <= 19 || found_letters[19]) && (i <= 20 || found_letters[20]) && (i <= 21 || found_letters[21]) && (i <= 22 || found_letters[22]) && (i <= 23 || found_letters[23]) && (i <= 24 || found_letters[24]) && (i <= 25 || found_letters[25])) {
        if (!found_letters[i]) {
            return 0;
        }
    }
    return 1;
}
