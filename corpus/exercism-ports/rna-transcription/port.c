#include "pfc.h"

/* Writes the RNA complement of `dna` to `rna`; returns 1, or 0 for a letter that is not a nucleotide, where
 * upstream frees its buffer and returns NULL. The buffer comes from the caller (P3); `switch` is an `if`
 * chain (P6). */
long transcribe(long n, const char dna[n], long m, char rna[m])
{
    for (long i = 0; i < n; i++) {
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
