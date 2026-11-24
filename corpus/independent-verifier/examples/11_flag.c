/* Hand transcription of examples/11_flag/flag.c. */
#define WIDTH 8
#define HEIGHT 5
#define WALL 4
#define FLAG_X 7
#define FLAG_Y 2

/*@ requires 0 <= x && x < WIDTH;
    terminates \false;
    assigns \nothing;
    ensures 0 <= \result && \result < WIDTH;
    ensures x - 1 <= \result && \result <= x + 1;
    ensures move == 2 || move == 3 || \result == x;
    ensures x >= WALL || \result < WALL;
*/
long step_x(long x, long move)
{
    if (move == 2 && x > 0) {
        return x - 1;
    }
    if (move == 3 && x + 1 < WIDTH && x + 1 != WALL) {
        return x + 1;
    }
    return x;
}

/*@ requires 0 <= y && y < HEIGHT;
    terminates \false;
    assigns \nothing;
    ensures 0 <= \result && \result < HEIGHT;
    ensures y - 1 <= \result && \result <= y + 1;
    ensures move == 0 || move == 1 || \result == y;
*/
long step_y(long y, long move)
{
    if (move == 0 && y > 0) {
        return y - 1;
    }
    if (move == 1 && y + 1 < HEIGHT) {
        return y + 1;
    }
    return y;
}

/*@ requires 0 <= n;
    requires \valid_read(moves + (0 .. n-1));
    terminates \false;
    assigns \nothing;
    ensures \result == 0;
*/
long play(long n, const long moves[n])
{
    long x = 0;
    long y = 2;
    long won = 0;
    /*@ loop invariant 0 <= i <= n;
        loop invariant 0 <= x && x < WIDTH && x < WALL && 0 <= y && y < HEIGHT && won == 0;
        loop assigns i, x, y, won;
    */
    for (long i = 0; i < n; i++) {
        x = step_x(x, moves[i]);
        y = step_y(y, moves[i]);
        if (x == FLAG_X && y == FLAG_Y) {
            won = 1;
        }
    }
    return won;
}

/*@ requires 0 <= n;
    requires \valid_read(moves + (0 .. n-1));
    terminates \false;
    assigns \nothing;
*/
void nobody_ever_wins(long n, const long moves[n])
{
    long r = play(n, moves);
    /*@ assert r == 0; */
}
