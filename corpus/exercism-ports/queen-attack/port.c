#include "pfc.h"

#define ROW_COUNT 8
#define COLUMN_COUNT 8
#define CAN_NOT_ATTACK 0
#define CAN_ATTACK 1
#define INVALID_POSITION 2

/* The two position structs become four parameters and the enum named constants (P5). */
long queens_attack(long white_row, long white_column, long black_row, long black_column)
{
    if ((white_column == black_column && white_row == black_row) || white_row >= ROW_COUNT ||
        white_column >= COLUMN_COUNT || black_row >= ROW_COUNT || black_column >= COLUMN_COUNT) {
        return INVALID_POSITION;
    }
    if (white_column == black_column || white_row == black_row ||
        (white_row - black_row == white_column - black_column) ||
        (white_row - black_row == black_column - white_column)) {
        return CAN_ATTACK;
    }
    return CAN_NOT_ATTACK;
}
