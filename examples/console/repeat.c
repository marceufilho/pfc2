#include "pfc.h"
#include "pfc_rt.h"

/* A function that takes a string and a count, called from `main`. C has no overloading, so printing a
 * string and printing a number are different functions. */
long greet(string name, long times)
    requires(0 <= times && times <= 1000)
{
    for (long i = 1; i <= times; i++) {
        print_str("Hello, ");
        println_str(name);
    }
    return 0;
}

int main(void)
{
    greet("PFC2", 3);
    return 0;
}
