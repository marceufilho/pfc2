/* No nonzero precondition. */
/*@  terminates \false;
    assigns \nothing; */
long division_zero(long d)
{
    /*@ assert division_denominator: d != 0; */
    return 1 / d;
}
