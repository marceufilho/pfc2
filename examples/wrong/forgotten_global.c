#include "pfc.h"

long hits = 0;

long hit(void)
    requires(hits < 1000)
{
    hits++;
    return hits;
}

/* `hit` writes `hits` and promises nothing about it, so the caller cannot know it afterwards.
 * Refused at line 19. */
long once(void)
    requires(hits == 0)
{
    hit();
    assert(hits == 1);
    return hits;
}
