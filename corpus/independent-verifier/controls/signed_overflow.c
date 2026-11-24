/* x=LONG_MAX makes the RTE overflow obligation invalid. */
/*@  terminates \false;
    assigns \nothing; */
long signed_overflow(long x)
{
    return x + 1;
}
