/* Independent ACSL transcription of kernels/matvec/kernel.c.
 * ACSL integer division agrees with positive C long division under these requires.
 * No bound on array contents or accumulator is added.
 */
/*@  requires 0 <= rows && 0 < cols && 0 <= matrix_len && rows <= matrix_len / cols;
    requires cols <= x_len && rows <= y_len;
    requires matrix_len > 0 ==> \valid_read(matrix + (0 .. matrix_len-1));
    requires x_len > 0 ==> \valid_read(x + (0 .. x_len-1));
    requires y_len > 0 ==> \valid(y + (0 .. y_len-1));
    requires \separated(matrix + (0 .. matrix_len-1), y + (0 .. y_len-1));
    requires \separated(x + (0 .. x_len-1), y + (0 .. y_len-1));
    terminates \false;
    assigns y[0 .. rows-1];
*/
long matvec(const long matrix[], long matrix_len, const long x[], long x_len,
            long y[], long y_len, long rows, long cols)
{
    /*@ assert division_contract: cols != 0 && !(matrix_len == (-9223372036854775807-1) && cols == -1); */
    long i = 0;
    /*@ loop invariant 0 <= i <= rows;
        loop assigns i, y[0 .. rows-1];
    */
    while (i < rows) {
        long s = 0;
        long j = 0;
        /*@ loop invariant 0 <= j <= cols;
            loop assigns j, s;
        */
        while (j < cols) {
            /*@ assert bounds_matrix: 0 <= i*cols+j < matrix_len; */
            /*@ assert bounds_x: 0 <= j < x_len; */
            s = s + matrix[i * cols + j] * x[j];
            j = j + 1;
        }
        /*@ assert bounds_y: 0 <= i < y_len; */
        y[i] = s;
        i = i + 1;
    }
    return rows;
}
