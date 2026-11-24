#include "pfc.h"

#define ONES 0
#define TWOS 1
#define THREES 2
#define FOURS 3
#define FIVES 4
#define SIXES 5
#define FULL_HOUSE 6
#define FOUR_OF_A_KIND 7
#define LITTLE_STRAIGHT 8
#define BIG_STRAIGHT 9
#define CHOICE 10
#define YACHT 11

/* The struct holding five faces is the array `faces` (P5); the struct of six counts that upstream returns by
 * value is an array the caller provides (P3); the enum is named constants; `switch` is an `if` chain (P6). */
long number_of_x(long n, const int faces[n], long x)
    requires(5 <= n && 0 <= x && x <= 6)
    ensures(result == x * ((faces[0] == x) + (faces[1] == x) + (faces[2] == x) + (faces[3] == x) + (faces[4] == x)))
{
    long sum = 0;

    for (long i = 0; i < 5; ++i) invariant(0 <= i && i <= 5 && (i != 0 || sum == x * 0) && (i != 1 || sum == x * ((faces[0] == x))) && (i != 2 || sum == x * ((faces[0] == x) + (faces[1] == x))) && (i != 3 || sum == x * ((faces[0] == x) + (faces[1] == x) + (faces[2] == x))) && (i != 4 || sum == x * ((faces[0] == x) + (faces[1] == x) + (faces[2] == x) + (faces[3] == x))) && (i != 5 || sum == x * ((faces[0] == x) + (faces[1] == x) + (faces[2] == x) + (faces[3] == x) + (faces[4] == x)))) {
        if (faces[i] == x) {
            sum += x;
        }
    }
    return sum;
}

long count(long n, const int faces[n], long m, long counts[m])
    requires(5 <= n && 6 <= m && 1 <= faces[0] && faces[0] <= 6 && 1 <= faces[1] && faces[1] <= 6 && 1 <= faces[2] && faces[2] <= 6 && 1 <= faces[3] && faces[3] <= 6 && 1 <= faces[4] && faces[4] <= 6)
{
    for (long i = 0; i < 5; ++i) invariant(0 <= i && i <= 5) {
        assert(faces[i] >= 1 && faces[i] <= 6);
        counts[faces[i] - 1] += 1;
    }
    return 0;
}

long has_count(long m, const long counts[m], long n)
    requires(6 <= m)
    ensures((result == 0 && counts[0] != n && counts[1] != n && counts[2] != n && counts[3] != n && counts[4] != n && counts[5] != n) || (1 <= result && result <= 6 && counts[result - 1] == n))
{
    for (long i = 0; i < 6; ++i) invariant(0 <= i && i <= 6 && (i <= 0 || counts[0] != n) && (i <= 1 || counts[1] != n) && (i <= 2 || counts[2] != n) && (i <= 3 || counts[3] != n) && (i <= 4 || counts[4] != n) && (i <= 5 || counts[5] != n)) {
        if (counts[i] == n) {
            return i + 1;
        }
    }
    return 0;
}

long sum(long n, const int faces[n])
    requires(5 <= n)
    ensures(result == (faces[0] + faces[1] + faces[2] + faces[3] + faces[4]))
{
    long s = 0;

    for (long i = 0; i < 5; ++i) invariant(0 <= i && i <= 5 && (i != 0 || s == 0) && (i != 1 || s == (faces[0])) && (i != 2 || s == (faces[0] + faces[1])) && (i != 3 || s == (faces[0] + faces[1] + faces[2])) && (i != 4 || s == (faces[0] + faces[1] + faces[2] + faces[3])) && (i != 5 || s == (faces[0] + faces[1] + faces[2] + faces[3] + faces[4]))) {
        s += faces[i];
    }
    return s;
}

long yacht_score(long n, const int faces[n], long category)
    requires(n == 5 && 1 <= faces[0] && faces[0] <= 6 && 1 <= faces[1] && faces[1] <= 6 && 1 <= faces[2] && faces[2] <= 6 && 1 <= faces[3] && faces[3] <= 6 && 1 <= faces[4] && faces[4] <= 6)
    ensures(category != ONES || result == 1 * ((faces[0] == 1) + (faces[1] == 1) + (faces[2] == 1) + (faces[3] == 1) + (faces[4] == 1)))
    ensures(category != TWOS || result == 2 * ((faces[0] == 2) + (faces[1] == 2) + (faces[2] == 2) + (faces[3] == 2) + (faces[4] == 2)))
    ensures(category != THREES || result == 3 * ((faces[0] == 3) + (faces[1] == 3) + (faces[2] == 3) + (faces[3] == 3) + (faces[4] == 3)))
    ensures(category != FOURS || result == 4 * ((faces[0] == 4) + (faces[1] == 4) + (faces[2] == 4) + (faces[3] == 4) + (faces[4] == 4)))
    ensures(category != FIVES || result == 5 * ((faces[0] == 5) + (faces[1] == 5) + (faces[2] == 5) + (faces[3] == 5) + (faces[4] == 5)))
    ensures(category != SIXES || result == 6 * ((faces[0] == 6) + (faces[1] == 6) + (faces[2] == 6) + (faces[3] == 6) + (faces[4] == 6)))
    ensures(category != FULL_HOUSE || result == 0 || result == (faces[0] + faces[1] + faces[2] + faces[3] + faces[4]))
    ensures(category != FOUR_OF_A_KIND || result == 0 || (4 <= result && result <= 24))
    ensures(category != LITTLE_STRAIGHT || result == 0 || result == 30)
    ensures(category != BIG_STRAIGHT || result == 0 || result == 30)
    ensures(category != CHOICE || result == (faces[0] + faces[1] + faces[2] + faces[3] + faces[4]))
    ensures(category != YACHT || result == 0 || result == 50)
{
    long counts[6] = {0};

    if (category == ONES) {
        return number_of_x(n, faces, 1);
    } else if (category == TWOS) {
        return number_of_x(n, faces, 2);
    } else if (category == THREES) {
        return number_of_x(n, faces, 3);
    } else if (category == FOURS) {
        return number_of_x(n, faces, 4);
    } else if (category == FIVES) {
        return number_of_x(n, faces, 5);
    } else if (category == SIXES) {
        return number_of_x(n, faces, 6);
    } else if (category == FULL_HOUSE) {
        count(n, faces, 6, counts);
        long three = has_count(6, counts, 3);
        long two = has_count(6, counts, 2);

        if (three && two) {
            return sum(n, faces);
        }
        return 0;
    } else if (category == FOUR_OF_A_KIND) {
        count(n, faces, 6, counts);
        long face_with_count_4 = has_count(6, counts, 4);
        long face_with_count_1 = has_count(6, counts, 1);
        long face_with_count_5 = has_count(6, counts, 5);

        if ((face_with_count_4 && face_with_count_1) || face_with_count_5) {
            return 4 * (face_with_count_4 + face_with_count_5);
        }
        return 0;
    } else if (category == LITTLE_STRAIGHT) {
        count(n, faces, 6, counts);
        for (long face = 0; face < 5; ++face) invariant(0 <= face && face <= 5) {
            if (counts[face] != 1) {
                return 0;
            }
        }
        return 30;
    } else if (category == BIG_STRAIGHT) {
        count(n, faces, 6, counts);
        for (long face = 1; face < 6; ++face) invariant(1 <= face && face <= 6) {
            if (counts[face] != 1) {
                return 0;
            }
        }
        return 30;
    } else if (category == CHOICE) {
        return sum(n, faces);
    } else if (category == YACHT) {
        count(n, faces, 6, counts);
        if (has_count(6, counts, 5)) {
            return 50;
        }
        return 0;
    }
    return 0;
}
