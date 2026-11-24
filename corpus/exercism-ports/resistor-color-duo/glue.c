/* Host C: the upstream interface on top of the port. Not verified. */
#include "resistor_color_duo.h"

long duo_code(long n, const int colors[]);

uint16_t color_code(resistor_band_t colors[])
{
   int two[2] = { (int)colors[0], (int)colors[1] };
   return (uint16_t)duo_code(2, two);
}
