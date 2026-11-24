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
{
    long sum = 0;

    for (long i = 0; i < 5; ++i) {
        if (faces[i] == x) {
            sum += x;
        }
    }
    return sum;
}

long count(long n, const int faces[n], long m, long counts[m])
{
    for (long i = 0; i < 5; ++i) {
        assert(faces[i] >= 1 && faces[i] <= 6);
        counts[faces[i] - 1] += 1;
    }
    return 0;
}

long has_count(long m, const long counts[m], long n)
{
    for (long i = 0; i < 6; ++i) {
        if (counts[i] == n) {
            return i + 1;
        }
    }
    return 0;
}

long sum(long n, const int faces[n])
{
    long s = 0;

    for (long i = 0; i < 5; ++i) {
        s += faces[i];
    }
    return s;
}

long yacht_score(long n, const int faces[n], long category)
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
        for (long face = 0; face < 5; ++face) {
            if (counts[face] != 1) {
                return 0;
            }
        }
        return 30;
    } else if (category == BIG_STRAIGHT) {
        count(n, faces, 6, counts);
        for (long face = 1; face < 6; ++face) {
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
