/* Initiation holds; preservation fails on odd n. */
/*@  requires 0 <= n <= 100; terminates \false;
    assigns \nothing; */
long bad_preservation(long n)
{
    long i = 0;
    /*@ loop invariant 0 <= i <= n;
        loop assigns i;
    */
    while (i < n) { i = i + 2; }
    return i;
}
