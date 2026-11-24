/* Host C: the upstream interface on top of the port. Not verified. */
#include "hello_world.h"

long hello_text(void);

const char *hello(void)
{
   static const char *texts[1] = { "Hello, World!" };
   return texts[hello_text()];
}
