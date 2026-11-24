#include "pfc.h"

/* Verina verina_basic_12: surface area of a cube with the given edge. */
long cubeSurfaceArea(long size)
    requires(size >= 0)
{
    return 6 * size * size;
}
