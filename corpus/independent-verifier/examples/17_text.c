/* Hand transcription of examples/17_text/text.c. The loop bounds PFC2 infers are written here. */
/*@ requires 0 <= n;
    requires \valid_read(s + (0 .. n-1));
    terminates \false;
    assigns \nothing;
    ensures 0 <= \result && \result <= n;
*/
long count_char(long n, const char s[n], long c)
{
    long found = 0;
    /*@ loop invariant 0 <= i <= n;
        loop invariant 0 <= found && found <= i;
        loop assigns i, found;
    */
    for (long i = 0; i < n; i++) {
        if (s[i] == c) {
            found++;
        }
    }
    return found;
}

/*@ requires 0 <= n;
    requires \valid_read(s + (0 .. n-1));
    terminates \false;
    assigns \nothing;
    ensures \result == -1 || (0 <= \result && \result < n && s[\result] == c);
*/
long index_of(long n, const char s[n], long c)
{
    long at = -1;
    /*@ loop invariant 0 <= i <= n;
        loop invariant at == -1;
        loop assigns i, at;
    */
    for (long i = 0; i < n; i++) {
        if (s[i] == c) {
            at = i;
            break;
        }
    }
    return at;
}

/*@ requires 0 <= n;
    requires \valid(s + (0 .. n-1));
    terminates \false;
    assigns s[0 .. n-1];
    ensures \result == n;
*/
long to_upper(long n, char s[n])
{
    /*@ loop invariant 0 <= i <= n;
        loop assigns i, s[0 .. n-1];
    */
    for (long i = 0; i < n; i++) {
        if (s[i] < 'a' || s[i] > 'z') {
            continue;
        }
        s[i] = s[i] - ('a' - 'A');
    }
    return n;
}

/*@ requires 0 <= d && d <= 9;
    terminates \false;
    assigns \nothing;
    ensures '0' <= \result && \result <= '9' && \result - '0' == d;
*/
long digit_char(long d)
{
    const char digits[11] = "0123456789";
    return digits[d];
}

/*@ requires 0 <= n;
    requires \valid_read(s + (0 .. n-1));
    terminates \false;
    assigns \nothing;
*/
void a_found_position_holds_the_character(long n, const char s[n], long c)
{
    long at = index_of(n, s, c);
    /*@ assert at == -1 || s[at] == c; */
}

/*@ requires n == 0;
    requires \valid_read(s + (0 .. n-1));
    terminates \false;
    assigns \nothing;
*/
void an_empty_text_contains_nothing(long n, const char s[n], long c)
{
    long r = count_char(n, s, c);
    /*@ assert r == 0; */
}

/*@ requires 0 <= d && d <= 9;
    terminates \false;
    assigns \nothing;
*/
void a_digit_survives_the_round_trip(long d)
{
    long r = digit_char(d);
    /*@ assert r - '0' == d; */
}
