#include "pfc.h"

#define BUCKET_ID_1 0
#define BUCKET_ID_2 1

/* Upstream keeps two `bucket_t {size, current}` structs and passes pointers to them. Here the two buckets are
 * the parallel arrays size[0..1] and current[0..1] (P5) and a pointer to a bucket is its index (P11). The
 * `void` functions return 0 and the MIN macro and `?:` are `if`s (P6, P14). */
long bucket_size(long k, const long size[k], long self)
    requires(k == 2 && 0 <= self && self <= 1)
    ensures(result == size[self])
{
    return size[self];
}

long bucket_current(long k, const long current[k], long self)
    requires(k == 2 && 0 <= self && self <= 1)
    ensures(result == current[self])
{
    return current[self];
}

_Bool bucket_is_empty(long k, const long current[k], long self)
    requires(k == 2 && 0 <= self && self <= 1)
    ensures(result == (current[self] == 0))
{
    return current[self] == 0;
}

_Bool bucket_is_full(long k, const long size[k], const long current[k], long self)
    requires(k == 2 && 0 <= self && self <= 1)
    ensures(result == (current[self] == size[self]))
{
    return current[self] == size[self];
}

_Bool bucket_contains(long k, const long current[k], long self, long amount)
    requires(k == 2 && 0 <= self && self <= 1)
    ensures(result == (current[self] == amount))
{
    return current[self] == amount;
}

long bucket_empty(long k, long current[k], long self)
    requires(k == 2 && 0 <= self && self <= 1)
    ensures(current[self] == 0)
{
    current[self] = 0;
    return 0;
}

long bucket_fill(long k, const long size[k], long current[k], long self)
    requires(k == 2 && 0 <= self && self <= 1 && separated(size, current))
    ensures(current[self] == size[self])
{
    current[self] = size[self];
    return 0;
}

long bucket_pour_into(long k, const long size[k], long current[k], long self, long other)
    requires(k == 2 && 0 <= self && self <= 1 && 0 <= other && other <= 1 && separated(size, current))
{
    long amount = size[other] - current[other];

    if (current[self] < size[other] - current[other]) {
        amount = current[self];
    }
    current[self] -= amount;
    current[other] += amount;
    return 0;
}

/* Upstream tests `bucket_contains` twice in the loop condition; the two calls are made before the loop and at
 * the end of its body, in the same order (P14). */
long solve(long k, const long size[k], long current[k], long goal_liters, long start_bucket)
    requires(k == 2 && separated(size, current) && 0 <= start_bucket && start_bucket <= 1)
    ensures(1 <= result)
{
    long max_moves = (bucket_size(k, size, 0) + 1) * (bucket_size(k, size, 1) + 1);
    long move_count = 0;
    long start = 1;
    long other = 1;

    if (start_bucket == BUCKET_ID_1) {
        start = 0;
    }
    if (start_bucket == BUCKET_ID_2) {
        other = 0;
    }
    bucket_fill(k, size, current, start);
    move_count += 1;
    _Bool start_has_goal = bucket_contains(k, current, start, goal_liters);
    _Bool other_has_goal = bucket_contains(k, current, other, goal_liters);

    while ((move_count <= max_moves) && !start_has_goal && !other_has_goal) invariant(1 <= move_count && 0 <= start && start <= 1 && 0 <= other && other <= 1) {
        if (bucket_size(k, size, other) == goal_liters) {
            bucket_fill(k, size, current, other);
        } else if (bucket_is_full(k, size, current, other)) {
            bucket_empty(k, current, other);
        } else if (!bucket_is_empty(k, current, start)) {
            bucket_pour_into(k, size, current, start, other);
        } else {
            bucket_fill(k, size, current, start);
        }
        move_count += 1;
        start_has_goal = bucket_contains(k, current, start, goal_liters);
        other_has_goal = bucket_contains(k, current, other, goal_liters);
    }
    return move_count;
}

/* The result struct {possible, move_count, goal_bucket, other_bucket_liters} is written to out[0..3] (P3,
 * P5); the fields upstream leaves at zero are zero. */
long measure_into(long bucket_1_size, long bucket_2_size, long goal_liters, long start_bucket, long m, long out[m])
    requires(4 <= m && 0 <= start_bucket && start_bucket <= 1)
    ensures(out[0] == 0 || out[0] == 1)
    ensures(out[0] == 1 || (out[1] == 0 && out[2] == 0 && out[3] == 0))
    ensures(out[0] == 0 || (1 <= out[1] && (out[2] == BUCKET_ID_1 || out[2] == BUCKET_ID_2)))
{
    long size[2] = {0, 0};
    long current[2] = {0, 0};

    size[0] = bucket_1_size;
    size[1] = bucket_2_size;
    out[0] = 0;
    out[1] = 0;
    out[2] = 0;
    out[3] = 0;
    long move_count = solve(2, size, current, goal_liters, start_bucket);

    if (bucket_contains(2, current, 0, goal_liters)) {
        out[0] = 1;
        out[1] = move_count;
        out[2] = BUCKET_ID_1;
        out[3] = bucket_current(2, current, 1);
    } else if (bucket_contains(2, current, 1, goal_liters)) {
        out[0] = 1;
        out[1] = move_count;
        out[2] = BUCKET_ID_2;
        out[3] = bucket_current(2, current, 0);
    } else {
        out[0] = 0;
    }
    return 0;
}
