#include "pfc.h"

/* Verina verina_advanced_62: units of rainwater trapped by an elevation map (two indices moving inwards). */
long rain(long heights_len, const long heights[heights_len])
{
    long left = 0;
    long right = heights_len - 1;
    long left_max = 0;
    long right_max = 0;
    long water = 0;

    while (left < right) {
        if (heights[left] < heights[right]) {
            if (heights[left] >= left_max) {
                left_max = heights[left];
            } else {
                water += left_max - heights[left];
            }
            left++;
        } else {
            if (heights[right] >= right_max) {
                right_max = heights[right];
            } else {
                water += right_max - heights[right];
            }
            right--;
        }
    }
    return water;
}
