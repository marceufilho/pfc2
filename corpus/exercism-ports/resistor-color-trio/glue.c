/* Host C: the upstream interface on top of the port. Not verified. */
#include "resistor_color_trio.h"

long trio_code(long n, const int colors[], long m, long resistor[]);

resistor_value_t color_code(resistor_band_t colors[])
{
   int three[3] = { (int)colors[0], (int)colors[1], (int)colors[2] };
   long resistor[2] = { 0, 0 };
   trio_code(3, three, 2, resistor);
   return (resistor_value_t){ (uint16_t)resistor[0], (resistor_unit_t)resistor[1] };
}
