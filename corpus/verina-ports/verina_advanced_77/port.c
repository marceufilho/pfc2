#include "pfc.h"

/* Verina verina_advanced_77: trapped water: at each index, the smaller of the highest elevation to its left
 * and to its right (itself included), minus its own elevation. */
long trapRainWater(long height_len, const long height[height_len])
{
    long water = 0;

    for (long i = 0; i < height_len; i++) {
        long left_max = height[i];
        long right_max = height[i];

        for (long j = 0; j < i; j++) {
            if (height[j] > left_max) {
                left_max = height[j];
            }
        }
        for (long j = i + 1; j < height_len; j++) {
            if (height[j] > right_max) {
                right_max = height[j];
            }
        }
        if (left_max < right_max) {
            water += left_max - height[i];
        } else {
            water += right_max - height[i];
        }
    }
    return water;
}
