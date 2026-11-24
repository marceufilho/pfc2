#include "pfc.h"

#define DIRECTION_NORTH 0
#define DIRECTION_DEFAULT 0
#define DIRECTION_EAST 1
#define DIRECTION_SOUTH 2
#define DIRECTION_WEST 3
#define DIRECTION_MAX 4

/* The robot struct {direction, {x, y}} is the array robot[0..2] (P3, P5); the enums are named constants;
 * `switch` is an `if` chain (P6); the `void` functions return 0 (P14). */
long robot_init(long direction, long x, long y, long m, long robot[m])
    requires(3 <= m)
    ensures(robot[1] == x && robot[2] == y)
    ensures((DIRECTION_NORTH <= direction && direction < DIRECTION_MAX && robot[0] == direction) || ((direction < DIRECTION_NORTH || direction >= DIRECTION_MAX) && robot[0] == DIRECTION_DEFAULT))
{
    robot[0] = direction;
    robot[1] = x;
    robot[2] = y;
    if ((direction < DIRECTION_NORTH) || (direction >= DIRECTION_MAX)) {
        robot[0] = DIRECTION_DEFAULT;
    }
    return 0;
}

long robot_turn_right(long m, long robot[m])
    requires(3 <= m && 0 <= robot[0] && robot[0] <= 3)
    ensures(0 <= robot[0] && robot[0] <= 3)
{
    robot[0] = (robot[0] + 1) % DIRECTION_MAX;
    return 0;
}

long robot_turn_left(long m, long robot[m])
    requires(3 <= m && 0 <= robot[0] && robot[0] <= 3)
    ensures(0 <= robot[0] && robot[0] <= 3)
{
    robot[0] = ((robot[0] - 1) + DIRECTION_MAX) % DIRECTION_MAX;
    return 0;
}

long robot_advance(long m, long robot[m])
    requires(3 <= m && 0 <= robot[0] && robot[0] <= 3)
    ensures(0 <= robot[0] && robot[0] <= 3)
{
    if (robot[0] == DIRECTION_NORTH) {
        robot[2]++;
    } else if (robot[0] == DIRECTION_EAST) {
        robot[1]++;
    } else if (robot[0] == DIRECTION_SOUTH) {
        robot[2]--;
    } else if (robot[0] == DIRECTION_WEST) {
        robot[1]--;
    }
    return 0;
}

/* The string of instructions arrives with its length (P2, P7 for strlen). */
long robot_run(long m, long robot[m], long n, const char instructions[n])
    requires(3 <= m && 0 <= robot[0] && robot[0] <= 3)
    ensures(0 <= robot[0] && robot[0] <= 3)
{
    for (long index = 0; index < n; index++) invariant(0 <= index && index <= n && 0 <= robot[0] && robot[0] <= 3) {
        long instruction = instructions[index];

        if (instruction == 'L') {
            robot_turn_left(m, robot);
        } else if (instruction == 'R') {
            robot_turn_right(m, robot);
        } else if (instruction == 'A') {
            robot_advance(m, robot);
        }
    }
    return 0;
}
