#include "pfc.h"

/* Text is an array of char with its length. A char is read as a small integer. */

/* How many of the n characters of s are c? Never more than n. */
long count_char(long n, const char s[n], long c)
    ensures(0 <= result && result <= n)
{
    long found = 0;

    for (long i = 0; i < n; i++) invariant(0 <= found && found <= i) {
        if (s[i] == c) {
            found++;
        }
    }
    return found;
}

/* Position of the first c, or -1 when there is none. */
long index_of(long n, const char s[n], long c)
    ensures(result == -1 || (0 <= result && result < n && s[result] == c))
{
    long at = -1;

    for (long i = 0; i < n; i++) invariant(at == -1) {
        if (s[i] == c) {
            at = i;
            break;
        }
    }
    return at;
}

/* Lower-case letters become upper case in place; every other character is skipped. */
long to_upper(long n, char s[n])
    ensures(result == n)
{
    for (long i = 0; i < n; i++) {
        if (s[i] < 'a' || s[i] > 'z') {
            continue;
        }
        s[i] = s[i] - ('a' - 'A');
    }
    return n;
}

/* The character that shows a digit. */
long digit_char(long d)
    requires(0 <= d && d <= 9)
    ensures('0' <= result && result <= '9' && result - '0' == d)
{
    const char digits[11] = "0123456789";

    return digits[d];
}

law a_found_position_holds_the_character(long n, const char s[n], long c)
{
    long at = index_of(n, s, c);

    assert(at == -1 || s[at] == c);
}

law an_empty_text_contains_nothing(long n where(n == 0), const char s[n], long c)
{
    assert(count_char(n, s, c) == 0);
}

law a_digit_survives_the_round_trip(long d where(0 <= d && d <= 9))
{
    assert(digit_char(d) - '0' == d);
}
