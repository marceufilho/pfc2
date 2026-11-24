/* Host C: the upstream interface on top of the port. Not verified. */
#include "robot_simulator.h"
#include <string.h>

long robot_init(long direction, long x, long y, long m, long robot[]);
long robot_run(long m, long robot[], long n, const char instructions[]);

robot_status_t robot_create(robot_direction_t direction, int x, int y)
{
   long robot[3] = { 0, 0, 0 };
   robot_init((long)(int)direction, x, y, 3, robot);
   return (robot_status_t){ (robot_direction_t)robot[0], { (int)robot[1], (int)robot[2] } };
}

void robot_move(robot_status_t *robot, const char *commands)
{
   long state[3] = { (long)(int)robot->direction, robot->position.x, robot->position.y };
   robot_run(3, state, (long)strlen(commands), commands);
   robot->direction = (robot_direction_t)state[0];
   robot->position.x = (int)state[1];
   robot->position.y = (int)state[2];
}
