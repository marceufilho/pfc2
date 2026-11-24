#include "pfc.h"
#include "pfc_rt.h"

/* An interactive program. The arithmetic is proved for the inputs the program accepts; reading and
 * printing go through pfc_rt.c, which is ordinary C and is listed as unverified. */
long divide(long x, long y)
    requires(y != 0)
    requires(-1000000 <= x && x <= 1000000)
{
    return x / y;
}

int main(void)
{
    println_str("two numbers, one per line:");
    long a = read_int();
    long b = read_int();

    if (a < -1000000 || a > 1000000 || b < -1000000 || b > 1000000) {
        println_str("too large");
        return 1;
    }
    print_str("sum ");
    print_int(a + b);
    println();
    print_str("product ");
    print_int(a * b);
    println();
    if (b != 0) {
        print_str("quotient ");
        print_int(divide(a, b));
        println();
    } else {
        println_str("no quotient: division by zero");
    }
    return 0;
}
