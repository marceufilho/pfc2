#include "pfc.h"

long matvec(const long matrix[], long matrix_len, const long x[], long x_len,
            long y[], long y_len, long rows, long cols)
{
    REQUIRES(0 <= rows && 0 < cols && 0 <= matrix_len && rows <= matrix_len / cols);
    REQUIRES(cols <= x_len && rows <= y_len);
    REQUIRES(SEPARATED(matrix, matrix_len, y, y_len));
    REQUIRES(SEPARATED(x, x_len, y, y_len));
    long i = 0;
    while (i < rows) {
        INVARIANT(0 <= i && i <= rows);
        long s = 0;
        long j = 0;
        while (j < cols) {
            INVARIANT(0 <= j && j <= cols);
            s = s + matrix[i * cols + j] * x[j];
            j = j + 1;
        }
        y[i] = s;
        i = i + 1;
    }
    return rows;
}
