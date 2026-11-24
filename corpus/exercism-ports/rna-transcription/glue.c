/* Host C: the upstream interface on top of the port. Not verified. */
#include "rna_transcription.h"
#include <stdlib.h>
#include <string.h>

long transcribe(long n, const char dna[], long m, char rna[]);

char *to_rna(const char *dna)
{
   size_t n = strlen(dna);
   char *rna = calloc(n + 1, sizeof(char));
   if (rna == NULL) {
      return NULL;
   }
   if (!transcribe((long)n, dna, (long)n + 1, rna)) {
      free(rna);
      return NULL;
   }
   return rna;
}
