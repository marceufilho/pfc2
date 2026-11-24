#include "pfc.h"

/* The Gregorian rule: every fourth year, except centuries, except every fourth century. */
long is_leap(long year)
    requires(1 <= year)
    ensures(result == 0 || result == 1)
    ensures((result == 1) == ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0))
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

long days_in_month(long year, long month)
    requires(1 <= year && 1 <= month && month <= 12)
    ensures(28 <= result && result <= 31)
    ensures(month != 2 || (result == 29) == ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0))
    ensures(month != 2 || result == 28 || result == 29)
{
    const long table[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    long days = table[month - 1];
    long leap = is_leap(year);

    if (month == 2 && leap == 1) {
        days++;
    }
    return days;
}

/* The position of a date in its year. The upper bound is loose on purpose: it is what the invariant
 * below states, and a law can only be as strong as the contract it rests on. */
long day_of_year(long year, long month, long day)
    requires(1 <= year && 1 <= month && month <= 12 && 1 <= day && day <= 31)
    ensures(day <= result && result <= day + 31 * (month - 1))
{
    long total = day;

    for (long m = 1; m < month; m++) invariant(day <= total && total <= day + 31 * (m - 1)) {
        total += days_in_month(year, m);
    }
    return total;
}

/* Laws: each holds for every year, not for the years somebody thought of testing. */

law every_400th_year_is_leap(long k where(1 <= k && k <= 1000000))
{
    assert(is_leap(400 * k) == 1);
}

law a_century_is_leap_only_when_divisible_by_400(long year where(1 <= year))
{
    long leap = is_leap(year);

    assert(year % 100 != 0 || year % 400 == 0 || leap == 0);
}

law february_has_one_more_day_exactly_in_leap_years(long year where(1 <= year))
{
    assert(days_in_month(year, 2) == 28 + is_leap(year));
}

law a_date_in_january_is_its_own_day_of_the_year(long year where(1 <= year), long day where(1 <= day && day <= 31))
{
    assert(day_of_year(year, 1, day) == day);
}
