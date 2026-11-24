#include "pfc.h"

/* The lock with a copy-and-paste slip: the last comparison reads keys[1] again instead of keys[3]. The right
 * combination opens it, and the usual wrong ones do not, so tests pass. The contract still claims that only
 * 3 1 4 1 opens it, and this file must be refused. */
long opens(long n, const long keys[n])
    requires(n == 4)
    ensures(result == 0 || result == 1)
    ensures(result == 0 || (keys[0] == 3 && keys[1] == 1 && keys[2] == 4 && keys[3] == 1))
    ensures(result == 1 || keys[0] != 3 || keys[1] != 1 || keys[2] != 4 || keys[3] != 1)
{
    if (keys[0] == 3 && keys[1] == 1 && keys[2] == 4 && keys[1] == 1) {
        return 1;
    }
    return 0;
}

law only_one_combination(long n where(n == 4), const long keys[n])
{
    assert(opens(n, keys) == 0 || (keys[0] == 3 && keys[1] == 1 && keys[2] == 4 && keys[3] == 1));
}
