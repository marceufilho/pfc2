#include "pfc.h"

/* tolower of the C locale, written out (P7). */
long to_lower(long c)
{
    if (c >= 'A' && c <= 'Z') {
        return c + ('a' - 'A');
    }
    return c;
}

/* Scrabble score of a word. The string arrives with its length (P2); upstream walks a pointer inside the
 * loop condition, `while ((c = tolower(*word++)) != '\0')`, which is an index and statements here (P11,
 * P14); its file-scope table is a local constant array (P14). */
long word_score_of(long n, const char word[n])
{
    const long score_book[26] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    long word_score = 0;
    long at = 0;

    while (at < n) {
        long current = word[at];
        long c = to_lower(current);

        at++;
        word_score += score_book[c - 'a'];
    }
    return word_score;
}
