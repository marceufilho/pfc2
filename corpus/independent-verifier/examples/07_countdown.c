/* Hand transcription of examples/07_countdown/countdown.c. The bound on `left` is the one PFC2 infers. */
/*@ requires 0 <= n;
    terminates \false;
    assigns \nothing;
    ensures \result == 0;
*/
long countdown(long n)
{
    long left = n;
    /*@ loop invariant 0 <= left <= n;
        loop assigns left;
        loop variant left;
    */
    while (left > 0) {
        left--;
    }
    return left;
}

/*@ requires 0 <= n;
    terminates \false;
    assigns \nothing;
*/
void every_countdown_reaches_zero(long n)
{
    long r = countdown(n);
    /*@ assert r == 0; */
}
