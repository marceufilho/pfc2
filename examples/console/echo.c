#include "pfc.h"
#include "pfc_rt.h"

/* Read a line and print it back. */
int main(void)
{
    print_str("What is your name? ");
    string name = read_line();

    print_str("Hello, ");
    println_str(name);
    return 0;
}
