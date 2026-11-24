#include "pfc.h"

/* Verina verina_advanced_77: trapped water: at each index, the smaller of the highest elevation to its left
 * and to its right (itself included), minus its own elevation. */
long trapRainWater(long height_len, const long height[height_len])
    ensures(result >= 0)
{
    long water = 0;

    for (long i = 0; i < height_len; i++) invariant(0 <= i && water >= 0) {
        long left_max = height[i];
        long right_max = height[i];

        for (long j = 0; j < i; j++) invariant(0 <= j && left_max >= height[i]) {
            if (height[j] > left_max) {
                left_max = height[j];
            }
        }
        for (long j = i + 1; j < height_len; j++) invariant(i + 1 <= j && right_max >= height[i]) {
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
