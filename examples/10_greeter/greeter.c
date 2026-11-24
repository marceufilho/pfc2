#include "pfc.h"
#include "pfc_rt.h"

/* Strings can be stored, passed, printed and compared. Nothing is proved about their characters. */
long greet(string name, long times)
    requires(0 <= times)
{
    for (long i = 0; i < times; i++) decreases(times - i) {
        print_str("hello, ");
        println_str(name);
    }
    return times;
}

int main(void)
{
    print_str("your name? ");
    string name = read_line();

    if (str_eq(name, "")) {
        name = "stranger";
    }
    greet(name, 2);
    return 0;
}
