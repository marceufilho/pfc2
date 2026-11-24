#include "pfc.h"

/* Writes the RNA complement of `dna` to `rna`; returns 1, or 0 for a letter that is not a nucleotide, where
 * upstream frees its buffer and returns NULL. The buffer comes from the caller (P3); `switch` is an `if`
 * chain (P6). */
long transcribe(long n, const char dna[n], long m, char rna[m])
    requires(n <= m && separated(rna, dna))
    ensures(result == 0 || result == 1)
    ensures(n != 0 || result == 1)
    ensures(result == 0 || n == 0 || (((dna[0] == 'G' && rna[0] == 'C') || (dna[0] == 'C' && rna[0] == 'G') || (dna[0] == 'T' && rna[0] == 'A') || (dna[0] == 'A' && rna[0] == 'U')) && ((dna[n - 1] == 'G' && rna[n - 1] == 'C') || (dna[n - 1] == 'C' && rna[n - 1] == 'G') || (dna[n - 1] == 'T' && rna[n - 1] == 'A') || (dna[n - 1] == 'A' && rna[n - 1] == 'U'))))
{
    for (long i = 0; i < n; i++) invariant(0 <= i && i <= n && (i == 0 || (((dna[0] == 'G' && rna[0] == 'C') || (dna[0] == 'C' && rna[0] == 'G') || (dna[0] == 'T' && rna[0] == 'A') || (dna[0] == 'A' && rna[0] == 'U')) && ((dna[i - 1] == 'G' && rna[i - 1] == 'C') || (dna[i - 1] == 'C' && rna[i - 1] == 'G') || (dna[i - 1] == 'T' && rna[i - 1] == 'A') || (dna[i - 1] == 'A' && rna[i - 1] == 'U'))))) {
        long base = dna[i];

        if (base == 'G') {
            rna[i] = 'C';
        } else if (base == 'C') {
            rna[i] = 'G';
        } else if (base == 'T') {
            rna[i] = 'A';
        } else if (base == 'A') {
            rna[i] = 'U';
        } else {
            return 0;
        }
    }
    return 1;
}
