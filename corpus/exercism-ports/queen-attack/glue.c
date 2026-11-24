/* Host C: the upstream interface on top of the port. Not verified. */
#include "queen_attack.h"

long queens_attack(long white_row, long white_column, long black_row, long black_column);

attack_status_t can_attack(position_t queen_1, position_t queen_2)
{
   return (attack_status_t)queens_attack(queen_1.row, queen_1.column, queen_2.row, queen_2.column);
}
