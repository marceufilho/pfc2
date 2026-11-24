/* Hand transcription of examples/16_calendar/calendar.c. */
/*@ requires 1 <= year;
    terminates \false;
    assigns \nothing;
    ensures \result == 0 || \result == 1;
    ensures (\result == 1) <==> ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0);
*/
long is_leap(long year)
{
    if (year % 400 == 0) {
        return 1;
    }
    if (year % 100 == 0) {
        return 0;
    }
    if (year % 4 == 0) {
        return 1;
    }
    return 0;
}

/*@ requires 1 <= year && 1 <= month && month <= 12;
    terminates \false;
    assigns \nothing;
    ensures 28 <= \result && \result <= 31;
    ensures month != 2
            || ((\result == 29) <==> ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0));
    ensures month != 2 || \result == 28 || \result == 29;
*/
long days_in_month(long year, long month)
{
    const long table[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    long days = table[month - 1];
    long leap = is_leap(year);
    if (month == 2 && leap == 1) {
        days++;
    }
    return days;
}

/*@ requires 1 <= year && 1 <= month && month <= 12 && 1 <= day && day <= 31;
    terminates \false;
    assigns \nothing;
    ensures day <= \result && \result <= day + 31 * (month - 1);
*/
long day_of_year(long year, long month, long day)
{
    long total = day;
    /*@ loop invariant 1 <= m <= month;
        loop invariant day <= total && total <= day + 31 * (m - 1);
        loop assigns m, total;
    */
    for (long m = 1; m < month; m++) {
        total += days_in_month(year, m);
    }
    return total;
}

/*@ requires 1 <= k && k <= 1000000;
    terminates \false;
    assigns \nothing;
*/
void every_400th_year_is_leap(long k)
{
    long leap = is_leap(400 * k);
    /*@ assert leap == 1; */
}

/*@ requires 1 <= year;
    terminates \false;
    assigns \nothing;
*/
void a_century_is_leap_only_when_divisible_by_400(long year)
{
    long leap = is_leap(year);
    /*@ assert year % 100 != 0 || year % 400 == 0 || leap == 0; */
}

/*@ requires 1 <= year;
    terminates \false;
    assigns \nothing;
*/
void february_has_one_more_day_exactly_in_leap_years(long year)
{
    long days = days_in_month(year, 2);
    long leap = is_leap(year);
    /*@ assert days == 28 + leap; */
}

/*@ requires 1 <= year;
    requires 1 <= day && day <= 31;
    terminates \false;
    assigns \nothing;
*/
void a_date_in_january_is_its_own_day_of_the_year(long year, long day)
{
    long r = day_of_year(year, 1, day);
    /*@ assert r == day; */
}
