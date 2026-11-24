#include "pfc.h"

/* A lock with four keys. Each right key advances it; a wrong key resets it. The combination is 3 1 4 1.
 * Two claims, proved for every input and not tried: the combination opens the lock, and nothing else does. */
long opens(long n, const long keys[n])
    requires(n == 4)
    ensures(result == 0 || result == 1)
    ensures(result == 0 || (keys[0] == 3 && keys[1] == 1 && keys[2] == 4 && keys[3] == 1))
    ensures(result == 1 || keys[0] != 3 || keys[1] != 1 || keys[2] != 4 || keys[3] != 1)
{
    long right = 0;

    /* The invariant below was proposed by a language model and admitted by the checker (model-proof.json). */
    for (long i = 0; i < n; i++)
        invariant(n == 4 && 0 <= i && i <= n && 0 <= right && right <= i &&
                  ((right == i) == ((i < 1 || keys[0] == 3) && (i < 2 || keys[1] == 1) && (i < 3 || keys[2] == 4) &&
                                    (i < 4 || keys[3] == 1))))
    {
        if ((i == 0 && keys[i] == 3) || (i == 1 && keys[i] == 1) || (i == 2 && keys[i] == 4) ||
            (i == 3 && keys[i] == 1)) {
            right = right + 1;
        } else {
            right = 0;
        }
    }
    if (right == 4) {
        return 1;
    }
    return 0;
}

law the_combination_opens(void)
{
    long keys[4] = {3, 1, 4, 1};
    assert(opens(4, keys) == 1);
}

law only_one_combination(long n where(n == 4), const long keys[n])
{
    assert(opens(n, keys) == 0 || (keys[0] == 3 && keys[1] == 1 && keys[2] == 4 && keys[3] == 1));
}
