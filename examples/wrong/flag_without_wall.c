#include "pfc.h"

/* The same game with the wall taken away (WALL is a column that does not exist). Now the flag can be
 * reached, so the claim "nobody ever wins" is false. Refused at line 52: one more move can break the
 * invariant, and the checker shows a state of the game from which it does. */
#define WIDTH 8
#define HEIGHT 5
#define WALL 99
#define FLAG_X 7
#define FLAG_Y 2

/* Moves: 0 up, 1 down, 2 left, 3 right. Any other number leaves the player where it is. */
long step_x(long x, long move)
    requires(0 <= x && x < WIDTH)
    ensures(0 <= result && result < WIDTH)
    ensures(x - 1 <= result && result <= x + 1)
    ensures(move == 2 || move == 3 || result == x)
    ensures(x >= WALL || result < WALL)
{
    if (move == 2 && x > 0) {
        return x - 1;
    }
    if (move == 3 && x + 1 < WIDTH && x + 1 != WALL) {
        return x + 1;
    }
    return x;
}

long step_y(long y, long move)
    requires(0 <= y && y < HEIGHT)
    ensures(0 <= result && result < HEIGHT)
    ensures(y - 1 <= result && result <= y + 1)
    ensures(move == 0 || move == 1 || result == y)
{
    if (move == 0 && y > 0) {
        return y - 1;
    }
    if (move == 1 && y + 1 < HEIGHT) {
        return y + 1;
    }
    return y;
}

/* 1 when the player stands on the flag after some move, 0 otherwise. */
long play(long n, const long moves[n])
    ensures(result == 0)
{
    long x = 0;
    long y = 2;
    long won = 0;

    for (long i = 0; i < n; i++) invariant(0 <= x && x < WIDTH && x < WALL && 0 <= y && y < HEIGHT && won == 0) {
        x = step_x(x, moves[i]);
        y = step_y(y, moves[i]);
        if (x == FLAG_X && y == FLAG_Y) {
            won = 1;
        }
    }
    return won;
}

/* The same claim as a law: whatever the moves, and however many, the flag is never taken. */
law nobody_ever_wins(long n where(0 <= n), const long moves[n])
{
    assert(play(n, moves) == 0);
}
