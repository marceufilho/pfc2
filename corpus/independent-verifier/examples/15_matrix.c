/* Hand transcription of examples/15_matrix/matrix.c. The loop bounds PFC2 infers are written here. */
#define N 3
#define CELLS 9

/*@ requires 0 <= i && i < N && 0 <= j && j < N;
    terminates \false;
    assigns \nothing;
    ensures \result == i * N + j;
    ensures 0 <= \result && \result < CELLS;
*/
long at(long i, long j)
{
    return i * N + j;
}

/*@ requires 0 <= cells;
    requires cells == CELLS;
    requires \valid_read(a + (0 .. cells-1));
    requires \valid_read(b + (0 .. cells-1));
    requires \valid(c + (0 .. cells-1));
    requires \separated(c + (0 .. cells-1), a + (0 .. cells-1));
    requires \separated(c + (0 .. cells-1), b + (0 .. cells-1));
    terminates \false;
    assigns c[0 .. cells-1];
*/
long multiply(long cells, const long a[cells], const long b[cells], long c[cells])
{
    /*@ loop invariant 0 <= i <= N;
        loop assigns i, c[0 .. cells-1];
    */
    for (long i = 0; i < N; i++) {
        /*@ loop invariant 0 <= j <= N;
            loop assigns j, c[0 .. cells-1];
        */
        for (long j = 0; j < N; j++) {
            long sum = 0;
            /*@ loop invariant 0 <= k <= N;
                loop assigns k, sum;
            */
            for (long k = 0; k < N; k++) {
                sum += a[at(i, k)] * b[at(k, j)];
            }
            c[at(i, j)] = sum;
        }
    }
    return 0;
}

/*@ requires -1000 <= a && a <= 1000 && -1000 <= b && b <= 1000;
    requires -1000 <= c && c <= 1000 && -1000 <= d && d <= 1000;
    terminates \false;
    assigns \nothing;
    ensures \result == a * d - b * c;
*/
long det2(long a, long b, long c, long d)
{
    return a * d - b * c;
}

/*@ requires 0 <= i && i < N && 0 <= j && j < N;
    requires 0 <= p && p < N && 0 <= q && q < N;
    terminates \false;
    assigns \nothing;
*/
void positions_do_not_collide(long i, long j, long p, long q)
{
    long one = at(i, j);
    long other = at(p, q);
    /*@ assert one != other || (i == p && j == q); */
}

/*@ requires 0 <= i && i < N - 1 && 0 <= j && j < N - 1;
    terminates \false;
    assigns \nothing;
*/
void cells_are_in_row_major_order(long i, long j)
{
    long right = at(i, j + 1);
    long here = at(i, j);
    /*@ assert right == here + 1; */
    long below = at(i + 1, 0);
    long last = at(i, N - 1);
    /*@ assert below == last + 1; */
}

/*@ requires 0 <= cell && cell < CELLS;
    terminates \false;
    assigns \nothing;
*/
void every_cell_is_a_position(long cell)
{
    long row = cell / N;
    long column = cell - row * N;
    long back = at(row, column);
    /*@ assert back == cell; */
}

/*@ requires -20 <= a && a <= 20 && -20 <= b && b <= 20 && -20 <= c && c <= 20 && -20 <= d && d <= 20;
    requires -20 <= e && e <= 20 && -20 <= f && f <= 20 && -20 <= g && g <= 20 && -20 <= h && h <= 20;
    terminates \false;
    assigns \nothing;
*/
void the_determinant_of_a_product_is_the_product_of_the_determinants(
    long a, long b, long c, long d, long e, long f, long g, long h)
{
    long p = a * e + b * g;
    long q = a * f + b * h;
    long r = c * e + d * g;
    long s = c * f + d * h;
    long product = det2(p, q, r, s);
    long first = det2(a, b, c, d);
    long second = det2(e, f, g, h);
    /*@ assert product == first * second; */
}
