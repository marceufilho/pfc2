#include "pfc.h"

#define NUMBER_OF_LETTERS 26

/* tolower and isalpha of the C locale, written out (P7). */
long to_lower(long c)
{
    if (c >= 'A' && c <= 'Z') {
        return c + ('a' - 'A');
    }
    return c;
}

_Bool is_alpha(long c)
{
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

/* Does the sentence use every letter. The string arrives with its length (P2); upstream's memset of the
 * table is its initial value (P7); the element is read into a local before the call (P13). */
_Bool pangram(long n, const char sentence[n])
{
    long sentence_length = n;
    _Bool found_letters[NUMBER_OF_LETTERS] = {0};

    for (long i = 0; i < sentence_length; i++) {
        long current = sentence[i];
        long letter = to_lower(current);

        if (is_alpha(letter)) {
            found_letters[letter - 'a'] = 1;
        }
    }
    for (long i = 0; i < NUMBER_OF_LETTERS; i++) {
        if (!found_letters[i]) {
            return 0;
        }
    }
    return 1;
}
