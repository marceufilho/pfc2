#include "pfc.h"

/* 3 x 3 matrices stored row by row in arrays of 9 cells. `at(i, j)` is where row i, column j lives.
 * Multiplication reads and writes through `at`, and every one of those accesses is proved inside its array.
 * Nothing bounds the numbers in the matrices, so the products and sums may overflow: the file certifies at
 * --level memory, with those two traps kept. The laws about the layout and the determinant are proved in full. */
#define N 3
#define CELLS 9

long at(long i, long j)
    requires(0 <= i && i < N && 0 <= j && j < N)
    ensures(result == i * N + j)
    ensures(0 <= result && result < CELLS)
{
    return i * N + j;
}

/* c = a * b. The result must not overlap the operands. */
long multiply(long cells, const long a[cells], const long b[cells], long c[cells])
    requires(cells == CELLS)
    requires(separated(c, a))
    requires(separated(c, b))
{
    for (long i = 0; i < N; i++) {
        for (long j = 0; j < N; j++) {
            long sum = 0;

            for (long k = 0; k < N; k++) {
                sum += a[at(i, k)] * b[at(k, j)];
            }
            c[at(i, j)] = sum;
        }
    }
    return 0;
}

/* The determinant of the 2 x 2 matrix [a b; c d]. */
long det2(long a, long b, long c, long d)
    requires(-1000 <= a && a <= 1000 && -1000 <= b && b <= 1000)
    requires(-1000 <= c && c <= 1000 && -1000 <= d && d <= 1000)
    ensures(result == a * d - b * c)
{
    return a * d - b * c;
}

/* Two different positions never share a cell: the layout loses nothing. */
law positions_do_not_collide(
    long i where(0 <= i && i < N), long j where(0 <= j && j < N),
    long p where(0 <= p && p < N), long q where(0 <= q && q < N))
{
    assert(at(i, j) != at(p, q) || (i == p && j == q));
}

/* Walking along a row moves one cell at a time, and the next row starts right after the last column. */
law cells_are_in_row_major_order(long i where(0 <= i && i < N - 1), long j where(0 <= j && j < N - 1))
{
    assert(at(i, j + 1) == at(i, j) + 1);
    assert(at(i + 1, 0) == at(i, N - 1) + 1);
}

/* Every cell is the position of exactly one row and column: decoding a cell and encoding it again gives
 * the cell back. With the law above, positions and cells correspond one to one. */
law every_cell_is_a_position(long cell where(0 <= cell && cell < CELLS))
{
    long row = cell / N;
    long column = cell - row * N;

    assert(at(row, column) == cell);
}

/* det(A * B) = det(A) * det(B), for every pair of 2 x 2 matrices with entries from -20 to 20:
 * about 6.5 trillion pairs of matrices, proved as one algebraic fact. */
law the_determinant_of_a_product_is_the_product_of_the_determinants(
    long a where(-20 <= a && a <= 20), long b where(-20 <= b && b <= 20),
    long c where(-20 <= c && c <= 20), long d where(-20 <= d && d <= 20),
    long e where(-20 <= e && e <= 20), long f where(-20 <= f && f <= 20),
    long g where(-20 <= g && g <= 20), long h where(-20 <= h && h <= 20))
{
    long p = a * e + b * g;
    long q = a * f + b * h;
    long r = c * e + d * g;
    long s = c * f + d * h;

    assert(det2(p, q, r, s) == det2(a, b, c, d) * det2(e, f, g, h));
}
