/* Initiation fails at n=0. */
/*@  requires 0 <= n; terminates \false;
    assigns \nothing; */
long false_invariant(long n)
{
    long i = 0;
    /*@ loop invariant 0 <= i < n;
        loop assigns i;
    */
    while (i < n) { i = i + 1; }
    return i;
}
