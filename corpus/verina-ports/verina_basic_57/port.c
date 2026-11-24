#include "pfc.h"

/* Verina verina_basic_57: number of elements of numbers that are less than threshold. */
long CountLessThan(long numbers_len, const long numbers[numbers_len], long threshold)
{
    long count = 0;

    for (long i = 0; i < numbers_len; i++) {
        if (numbers[i] < threshold) {
            count++;
        }
    }
    return count;
}
