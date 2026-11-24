/* Hand transcription of examples/08_counter/counter.c. The write sets PFC2 computes are the assigns clauses. */
long hits = 0;
long limit = 100;

/*@ requires 0 <= hits;
    terminates \false;
    assigns hits;
    ensures 0 <= hits;
    ensures \result == hits;
*/
long hit(void)
{
    if (hits < limit) {
        hits++;
    }
    return hits;
}

/*@ requires 0 <= hits;
    terminates \false;
    assigns hits;
*/
long twice(void)
{
    long before = limit;
    hit();
    hit();
    /*@ assert limit == before; */
    return hits;
}
