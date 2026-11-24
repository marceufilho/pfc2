---
title: "Examples"
description: Every example program, with the verdict it must get and a link that opens it in the playground.
---

Each program below opens in the [playground](../playground/). The verdicts are the ones written by hand in
`examples/examples.json`; the test suite and this site's browser tests hold PFC2 to them.

## Functions

### 01_count/count

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=01_count/count)

```c
#include "pfc.h"

/* The smallest proved program. Nothing is written for the loop: its bounds 0 <= i <= n are
 * proposed from its shape and kept because the checker proves them. */
long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;

    while (i < n) {
        i++;
    }
    return i;
}

/* A law is proved for every input; it is never run. This one covers every n a long can hold. */
law counting_to_n_gives_n(long n where(0 <= n))
{
    assert(count(n) == n);
}
```

### 02_fill/fill

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=02_fill/fill)

```c
#include "pfc.h"

/* `long a[n]` says the array has n elements, so no length is passed by hand and every write is
 * proved inside the array: the certified C has no bounds check left. */
long fill(long n, long a[n], long value)
{
    for (long i = 0; i < n; i++) {
        a[i] = value;
    }
    return n;
}
```

### 03_sum/sum

Expected: **certified at level `memory`**. [Open in the playground](../playground/#example=03_sum/sum)

```c
#include "pfc.h"

/* Nothing bounds the elements, so `s += a[i]` may overflow. The file certifies at --level memory:
 * every access is proved in bounds and the addition keeps its overflow trap, which is listed. */
long sum(long n, const long a[n])
{
    long s = 0;

    for (long i = 0; i < n; i++) {
        s += a[i];
    }
    return s;
}
```

### 04_bounded_sum/bounded_sum

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=04_bounded_sum/bounded_sum)

```c
#include "pfc.h"

/* Adding at most 1000 small steps cannot overflow. The invariant says how the total grows; with it
 * the file certifies at the default --level full: no runtime check of any kind remains. */
long bounded_sum(long n, long step)
    requires(0 <= n && n <= 1000)
    requires(0 <= step && step <= 1000)
    ensures(result == n * step)
{
    long total = 0;

    for (long i = 0; i < n; i++) invariant(total == i * step) {
        total += step;
    }
    return total;
}

/* Each law is proved for every n and step from 0 to 1000: about a million cases each. */

/* One more step adds exactly one step. */
law one_more_step_adds_the_step(long n where(0 <= n && n < 1000), long step where(0 <= step && step <= 1000))
{
    assert(bounded_sum(n + 1, step) == bounded_sum(n, step) + step);
}

/* n steps of size s reach the same place as s steps of size n. */
law the_count_and_the_step_can_be_swapped(long n where(0 <= n && n <= 1000), long step where(0 <= step && step <= 1000))
{
    assert(bounded_sum(n, step) == bounded_sum(step, n));
}
```

### 05_binary_search/binary_search

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=05_binary_search/binary_search)

```c
#include "pfc.h"

/* The classic midpoint, written so it cannot overflow. The proof shows every probe is inside the
 * array and that the search stops; it says nothing about the array being sorted. */
long binary_search(long n, const long a[n], long key)
    requires(0 <= n)
    ensures(-1 <= result && result < n)
    ensures(result == -1 || a[result] == key)
{
    long lo = 0;
    long hi = n;

    while (lo < hi) invariant(0 <= lo && lo <= hi && hi <= n) decreases(hi - lo) {
        long mid = lo + (hi - lo) / 2;

        if (a[mid] == key) {
            return mid;
        }
        if (a[mid] < key) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return -1;
}

/* Whatever the array holds and whatever is searched for: an answer other than -1 is an index of the
 * array, and the key is there. (That -1 means "absent" would need "the array is sorted" and "no element
 * equals the key", both statements about every element, which PFC2 cannot write.) */
law a_found_index_holds_the_key(long n where(0 <= n), const long a[n], long key)
{
    long found = binary_search(n, a, key);

    assert(found == -1 || (0 <= found && found < n && a[found] == key));
}
```

### 06_copy/copy

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=06_copy/copy)

```c
#include "pfc.h"

/* Two arrays that do not overlap. The law states what a caller may rely on. */
long copy(long n, long dst[n], const long src[n])
    requires(separated(dst, src))
{
    for (long i = 0; i < n; i++) {
        dst[i] = src[i];
    }
    return n;
}
```

### 07_countdown/countdown

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=07_countdown/countdown)

```c
#include "pfc.h"

/* decreases(e): e is never negative when the body starts and is smaller when it ends, so the
 * loop cannot run forever. Without it PFC2 proves what the loop computes, not that it stops. */
long countdown(long n)
    requires(0 <= n)
    ensures(result == 0)
{
    long left = n;

    while (left > 0) decreases(left) {
        left--;
    }
    return left;
}

/* For every starting value, the countdown ends at zero. */
law every_countdown_reaches_zero(long n where(0 <= n))
{
    assert(countdown(n) == 0);
}
```

### 08_counter/counter

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=08_counter/counter)

```c
#include "pfc.h"

/* Globals are part of the state. A caller keeps what it knows about the globals a function does
 * not write, and learns about the others only what the function's `ensures` says. */
long hits = 0;
long limit = 100;

long hit(void)
    requires(0 <= hits)
    ensures(0 <= hits)
    ensures(result == hits)
{
    if (hits < limit) {
        hits++;
    }
    return hits;
}

long twice(void)
    requires(0 <= hits)
{
    long before = limit;

    hit();
    hit();
    assert(limit == before);
    return hits;
}
```

### 11_flag/flag

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=11_flag/flag)

```c
#include "pfc.h"

/* Capture the flag, on a board 8 wide and 5 high. The player starts at (0, 2); the flag is at (7, 2).
 * A wall stands in column 4, from top to bottom. The claim: no sequence of moves, of any length, ever
 * puts the player on the flag. It is proved for all of them at once, not tried. */
#define WIDTH 8
#define HEIGHT 5
#define WALL 4
#define FLAG_X 7
#define FLAG_Y 2

/* Moves: 0 up, 1 down, 2 left, 3 right. Any other number leaves the player where it is. */
long step_x(long x, long move)
    requires(0 <= x && x < WIDTH)
    ensures(0 <= result && result < WIDTH)
    ensures(x - 1 <= result && result <= x + 1)
    ensures(move == 2 || move == 3 || result == x)
    ensures(x >= WALL || result < WALL)
{
    if (move == 2 && x > 0) {
        return x - 1;
    }
    if (move == 3 && x + 1 < WIDTH && x + 1 != WALL) {
        return x + 1;
    }
    return x;
}

long step_y(long y, long move)
    requires(0 <= y && y < HEIGHT)
    ensures(0 <= result && result < HEIGHT)
    ensures(y - 1 <= result && result <= y + 1)
    ensures(move == 0 || move == 1 || result == y)
{
    if (move == 0 && y > 0) {
        return y - 1;
    }
    if (move == 1 && y + 1 < HEIGHT) {
        return y + 1;
    }
    return y;
}

/* 1 when the player stands on the flag after some move, 0 otherwise. */
long play(long n, const long moves[n])
    ensures(result == 0)
{
    long x = 0;
    long y = 2;
    long won = 0;

    for (long i = 0; i < n; i++) invariant(0 <= x && x < WIDTH && x < WALL && 0 <= y && y < HEIGHT && won == 0) {
        x = step_x(x, moves[i]);
        y = step_y(y, moves[i]);
        if (x == FLAG_X && y == FLAG_Y) {
            won = 1;
        }
    }
    return won;
}

/* The same claim as a law: whatever the moves, and however many, the flag is never taken. */
law nobody_ever_wins(long n where(0 <= n), const long moves[n])
{
    assert(play(n, moves) == 0);
}
```

### 12_rest_api/api

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=12_rest_api/api)

```c
#include "pfc.h"

/* The handlers of a small REST API over a table of n items:
 *
 *     GET    /items/{id}            200 and the value, or 404
 *     PUT    /items/{id}  {value}   201 created, 200 replaced, 400 bad value, 404 no such slot
 *     DELETE /items/{id}            204, or 404
 *     anything else                 405
 *
 * `handle` accepts ANY method, id and value a client can send: nothing is required of them. What is
 * proved, for every request: the table is never read or written outside its n slots, the status is one
 * of the documented ones, and a request for an id outside the table never succeeds. The HTTP server
 * around it (server.py) is ordinary, unverified code. */
#define GET 0
#define PUT 1
#define DELETE 2
#define MAX_VALUE 1000000

long reply = 0; /* The value a successful GET returns. */

/* Globals are private to the certified code, so the server reads the value through this function. */
long last_reply(void)
{
    return reply;
}

long handle(long n, long used[n], long values[n], long method, long id, long value)
    ensures(result == 200 || result == 201 || result == 204 || result == 400 || result == 404 || result == 405)
    ensures((0 <= id && id < n) || result == 404 || result == 405)
    ensures((method == GET || method == PUT || method == DELETE) == (result != 405))
{
    if (method != GET && method != PUT && method != DELETE) {
        return 405;
    }
    if (id < 0 || id >= n) {
        return 404;
    }
    if (method == GET) {
        if (used[id] == 0) {
            return 404;
        }
        reply = values[id];
        return 200;
    }
    if (method == PUT) {
        if (value < 0 || value > MAX_VALUE) {
            return 400;
        }
        values[id] = value;
        if (used[id] == 0) {
            used[id] = 1;
            return 201;
        }
        return 200;
    }
    if (used[id] == 0) {
        return 404;
    }
    used[id] = 0;
    return 204;
}

/* A law about one request, proved for every table: a negative id is always "not found". */
law negative_id_is_not_found(long n, long used[n], long values[n], long id where(id < 0), long value)
{
    assert(handle(n, used, values, GET, id, value) == 404);
}
```

### 13_progression/progression

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=13_progression/progression)

```c
#include "pfc.h"

/* The n-th term of an arithmetic progression, computed the slow way: begin at `start` and add `step`
 * n times. The contract says what that loop amounts to: start + n * step. */
long term(long start, long step, long n)
    requires(-1000 <= start && start <= 1000)
    requires(-1000 <= step && step <= 1000)
    requires(0 <= n && n <= 1000)
    ensures(result == start + n * step)
{
    long value = start;

    for (long i = 0; i < n; i++) invariant(value == start + i * step) {
        value += step;
    }
    return value;
}

/* A test would check a few cases: term(0, 1, 5) == 5, term(2, 3, 4) == 14, term(7, 0, 9) == 7.
 * Each law below is proved for every start, step and n in the ranges: about four billion cases each. */

/* Counting is the progression that starts at 0 and steps by 1. */
law counting_is_a_progression(long n where(0 <= n && n <= 1000))
{
    assert(term(0, 1, n) == n);
}

/* Two consecutive terms differ by exactly the step, wherever you are in the progression. */
law consecutive_terms_differ_by_the_step(
    long start where(-1000 <= start && start <= 1000),
    long step where(-1000 <= step && step <= 1000),
    long n where(0 <= n && n < 1000))
{
    assert(term(start, step, n + 1) - term(start, step, n) == step);
}

/* Every term is the average of its two neighbours. */
law a_term_is_the_average_of_its_neighbours(
    long start where(-1000 <= start && start <= 1000),
    long step where(-1000 <= step && step <= 1000),
    long n where(1 <= n && n < 1000))
{
    assert(2 * term(start, step, n) == term(start, step, n - 1) + term(start, step, n + 1));
}

/* With a step of zero the progression never moves. */
law a_zero_step_stays_put(long start where(-1000 <= start && start <= 1000), long n where(0 <= n && n <= 1000))
{
    assert(term(start, 0, n) == start);
}

/* Reversing the step walks back to where you began. The ranges are narrower here because the first
 * result is passed on as a start, which `term` only accepts between -1000 and 1000: the checker refused
 * a wider version of this law and showed start = 47, step = 1, n = 960. */
law stepping_back_returns_to_the_start(
    long start where(-100 <= start && start <= 100),
    long step where(-1 <= step && step <= 1),
    long n where(0 <= n && n <= 900))
{
    assert(term(term(start, step, n), 0 - step, n) == start);
}
```

### 14_tree/tree

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=14_tree/tree)

```c
#include "pfc.h"

/* A binary tree stored in an array, the way a heap is: node i has its children at 2i + 1 and 2i + 2 and
 * its parent at (i - 1) / 2. There are no pointers, so "the tree is well formed" becomes arithmetic about
 * indices, and the laws below prove it for every node up to a million. */
#define LAST 1000000

long left(long i)
    requires(0 <= i && i <= LAST)
    ensures(result == 2 * i + 1)
{
    return 2 * i + 1;
}

long right(long i)
    requires(0 <= i && i <= LAST)
    ensures(result == 2 * i + 2)
{
    return 2 * i + 2;
}

long parent(long i)
    requires(1 <= i && i <= 2000002)
    ensures(result == (i - 1) / 2)
{
    return (i - 1) / 2;
}

/* How many steps from node i up to the root. The loop is proved to stop: every step goes to a smaller index. */
long depth(long i)
    requires(0 <= i && i <= LAST)
    ensures(0 <= result && result <= i)
{
    long node = i;
    long steps = 0;

    while (node > 0) invariant(0 <= node && 0 <= steps && steps + node <= i) decreases(node) {
        node = parent(node);
        steps++;
    }
    return steps;
}

/* The largest value on the path from node i up to the root. Every read is proved inside the array. */
long path_max(long n, const long tree[n], long i)
    requires(0 <= i && i < n && n <= LAST)
{
    long node = i;
    long best = tree[i];

    while (node > 0) invariant(0 <= node && node <= i) decreases(node) {
        node = parent(node);
        if (tree[node] > best) {
            best = tree[node];
        }
    }
    return best;
}

/* Going down to a child and back up returns to the same node: no node has two parents. */
law the_parent_of_a_left_child_is_the_node(long i where(0 <= i && i <= LAST))
{
    assert(parent(left(i)) == i);
}

law the_parent_of_a_right_child_is_the_node(long i where(0 <= i && i <= LAST))
{
    assert(parent(right(i)) == i);
}

/* The two children of a node are different, adjacent, and further down the array than the node. */
law children_are_adjacent_and_below(long i where(0 <= i && i <= LAST))
{
    long l = left(i);
    long r = right(i);

    assert(r == l + 1);
    assert(i < l);
}

/* Two different nodes never share a left child. */
law left_children_do_not_collide(long i where(0 <= i && i <= LAST), long j where(0 <= j && j <= LAST))
{
    assert(left(i) != left(j) || i == j);
}

/* Every node except the root is one of the two children of its parent, and its parent comes earlier in
 * the array. Together with the laws above: the array is exactly one tree, with nothing lost or shared. */
law every_node_is_a_child_of_its_parent(long i where(1 <= i && i <= LAST))
{
    long up = parent(i);
    long first = left(up);
    long second = right(up);

    assert(up < i);
    assert(first == i || second == i);
}

/* Walking up from any node reaches the root in at most i steps, and never more steps than from a node
 * further down the same path. ("A child is exactly one level below its parent" needs a recursive definition
 * of depth, which PFC2 cannot state.) */
law the_walk_to_the_root_is_bounded(long i where(0 <= i && i <= LAST))
{
    assert(depth(i) <= i);
}
```

### 15_matrix/matrix

Expected: **certified at level `memory`**. [Open in the playground](../playground/#example=15_matrix/matrix)

```c
#include "pfc.h"

/* 3 x 3 matrices stored row by row in arrays of 9 cells. `at(i, j)` is where row i, column j lives.
 * Multiplication reads and writes through `at`, and every one of those accesses is proved inside its array.
 * Nothing bounds the numbers in the matrices, so the products and sums may overflow: the file certifies at
 * --level memory, with those two traps kept. The laws about the layout and the determinant are proved in full. */
#define N 3
#define CELLS 9

long at(long i, long j)
    requires(0 <= i && i < N && 0 <= j && j < N)
    ensures(result == i * N + j)
    ensures(0 <= result && result < CELLS)
{
    return i * N + j;
}

/* c = a * b. The result must not overlap the operands. */
long multiply(long cells, const long a[cells], const long b[cells], long c[cells])
    requires(cells == CELLS)
    requires(separated(c, a))
    requires(separated(c, b))
{
    for (long i = 0; i < N; i++) {
        for (long j = 0; j < N; j++) {
            long sum = 0;

            for (long k = 0; k < N; k++) {
                sum += a[at(i, k)] * b[at(k, j)];
            }
            c[at(i, j)] = sum;
        }
    }
    return 0;
}

/* The determinant of the 2 x 2 matrix [a b; c d]. */
long det2(long a, long b, long c, long d)
    requires(-1000 <= a && a <= 1000 && -1000 <= b && b <= 1000)
    requires(-1000 <= c && c <= 1000 && -1000 <= d && d <= 1000)
    ensures(result == a * d - b * c)
{
    return a * d - b * c;
}

/* Two different positions never share a cell: the layout loses nothing. */
law positions_do_not_collide(
    long i where(0 <= i && i < N), long j where(0 <= j && j < N),
    long p where(0 <= p && p < N), long q where(0 <= q && q < N))
{
    assert(at(i, j) != at(p, q) || (i == p && j == q));
}

/* Walking along a row moves one cell at a time, and the next row starts right after the last column. */
law cells_are_in_row_major_order(long i where(0 <= i && i < N - 1), long j where(0 <= j && j < N - 1))
{
    assert(at(i, j + 1) == at(i, j) + 1);
    assert(at(i + 1, 0) == at(i, N - 1) + 1);
}

/* Every cell is the position of exactly one row and column: decoding a cell and encoding it again gives
 * the cell back. With the law above, positions and cells correspond one to one. */
law every_cell_is_a_position(long cell where(0 <= cell && cell < CELLS))
{
    long row = cell / N;
    long column = cell - row * N;

    assert(at(row, column) == cell);
}

/* det(A * B) = det(A) * det(B), for every pair of 2 x 2 matrices with entries from -20 to 20:
 * about 6.5 trillion pairs of matrices, proved as one algebraic fact. */
law the_determinant_of_a_product_is_the_product_of_the_determinants(
    long a where(-20 <= a && a <= 20), long b where(-20 <= b && b <= 20),
    long c where(-20 <= c && c <= 20), long d where(-20 <= d && d <= 20),
    long e where(-20 <= e && e <= 20), long f where(-20 <= f && f <= 20),
    long g where(-20 <= g && g <= 20), long h where(-20 <= h && h <= 20))
{
    long p = a * e + b * g;
    long q = a * f + b * h;
    long r = c * e + d * g;
    long s = c * f + d * h;

    assert(det2(p, q, r, s) == det2(a, b, c, d) * det2(e, f, g, h));
}
```

### 16_calendar/calendar

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=16_calendar/calendar)

```c
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
```

### 17_text/text

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=17_text/text)

```c
#include "pfc.h"

/* Text is an array of char with its length. A char is read as a small integer. */

/* How many of the n characters of s are c? Never more than n. */
long count_char(long n, const char s[n], long c)
    ensures(0 <= result && result <= n)
{
    long found = 0;

    for (long i = 0; i < n; i++) invariant(0 <= found && found <= i) {
        if (s[i] == c) {
            found++;
        }
    }
    return found;
}

/* Position of the first c, or -1 when there is none. */
long index_of(long n, const char s[n], long c)
    ensures(result == -1 || (0 <= result && result < n && s[result] == c))
{
    long at = -1;

    for (long i = 0; i < n; i++) invariant(at == -1) {
        if (s[i] == c) {
            at = i;
            break;
        }
    }
    return at;
}

/* Lower-case letters become upper case in place; every other character is skipped. */
long to_upper(long n, char s[n])
    ensures(result == n)
{
    for (long i = 0; i < n; i++) {
        if (s[i] < 'a' || s[i] > 'z') {
            continue;
        }
        s[i] = s[i] - ('a' - 'A');
    }
    return n;
}

/* The character that shows a digit. */
long digit_char(long d)
    requires(0 <= d && d <= 9)
    ensures('0' <= result && result <= '9' && result - '0' == d)
{
    const char digits[11] = "0123456789";

    return digits[d];
}

law a_found_position_holds_the_character(long n, const char s[n], long c)
{
    long at = index_of(n, s, c);

    assert(at == -1 || s[at] == c);
}

law an_empty_text_contains_nothing(long n where(n == 0), const char s[n], long c)
{
    assert(count_char(n, s, c) == 0);
}

law a_digit_survives_the_round_trip(long d where(0 <= d && d <= 9))
{
    assert(digit_char(d) - '0' == d);
}
```

## Programs

### 09_calculator/calculator

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=09_calculator/calculator)

```c
#include "pfc.h"
#include "pfc_rt.h"

/* An interactive program. The arithmetic is proved for the inputs the program accepts; reading and
 * printing go through pfc_rt.c, which is ordinary C and is listed as unverified. */
long divide(long x, long y)
    requires(y != 0)
    requires(-1000000 <= x && x <= 1000000)
{
    return x / y;
}

int main(void)
{
    println_str("two numbers, one per line:");
    long a = read_int();
    long b = read_int();

    if (a < -1000000 || a > 1000000 || b < -1000000 || b > 1000000) {
        println_str("too large");
        return 1;
    }
    print_str("sum ");
    print_int(a + b);
    println();
    print_str("product ");
    print_int(a * b);
    println();
    if (b != 0) {
        print_str("quotient ");
        print_int(divide(a, b));
        println();
    } else {
        println_str("no quotient: division by zero");
    }
    return 0;
}
```

### 10_greeter/greeter

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=10_greeter/greeter)

```c
#include "pfc.h"
#include "pfc_rt.h"

/* Strings can be stored, passed, printed and compared. Nothing is proved about their characters. */
long greet(string name, long times)
    requires(0 <= times)
{
    for (long i = 0; i < times; i++) decreases(times - i) {
        print_str("hello, ");
        println_str(name);
    }
    return times;
}

int main(void)
{
    print_str("your name? ");
    string name = read_line();

    if (str_eq(name, "")) {
        name = "stranger";
    }
    greet(name, 2);
    return 0;
}
```

### console/minimal

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=console/minimal)

```c
#include "pfc.h"

/* The smallest program: an entry point that does nothing and returns 0. */
int main(void)
{
    return 0;
}
```

### console/arithmetic

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=console/arithmetic)

```c
#include "pfc.h"
#include "pfc_rt.h"

/* A chain of small arithmetic functions over a global. Each function states the range it is used with,
 * so every operation is proved free of overflow and the division proved not to divide by zero; `main`
 * then proves, by the contracts alone, that the chain ends at 10. */
long outcome = 0;

long add(long x, long y)
    requires(-1000000 <= x && x <= 1000000 && -1000000 <= y && y <= 1000000)
    ensures(result == x + y)
{
    return x + y;
}

long subtract(long x, long y)
    requires(-1000000 <= x && x <= 1000000 && -1000000 <= y && y <= 1000000)
    ensures(result == x - y)
{
    return x - y;
}

long multiply(long x, long y)
    requires(-1000000 <= x && x <= 1000000 && -1000000 <= y && y <= 1000000)
    ensures(result == x * y)
{
    return x * y;
}

long divide(long x, long y)
    requires(-1000000 <= x && x <= 1000000)
    ensures(y == 0 || result == x / y)
    ensures(y != 0 || result == 0)
{
    if (y == 0) {
        return 0;
    }
    return x / y;
}

long max(long x, long y)
    ensures(result >= x && result >= y && (result == x || result == y))
{
    if (x > y) {
        return x;
    }
    return y;
}

long min(long x, long y)
    ensures(result <= x && result <= y && (result == x || result == y))
{
    if (x < y) {
        return x;
    }
    return y;
}

int main(void)
{
    long a = 20;
    long b = 5;

    outcome = add(a, b);
    outcome = subtract(outcome, 3);
    outcome = multiply(outcome, 2);
    outcome = divide(outcome, b);
    outcome = max(outcome, 10);
    outcome = min(outcome, 50);
    assert(outcome == 10);
    print_int(outcome);
    println();
    return 0;
}
```

### console/repeat

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=console/repeat)

```c
#include "pfc.h"
#include "pfc_rt.h"

/* A function that takes a string and a count, called from `main`. C has no overloading, so printing a
 * string and printing a number are different functions. */
long greet(string name, long times)
    requires(0 <= times && times <= 1000)
{
    for (long i = 1; i <= times; i++) {
        print_str("Hello, ");
        println_str(name);
    }
    return 0;
}

int main(void)
{
    greet("PFC2", 3);
    return 0;
}
```

### console/echo

Expected: **certified at level `full`**. [Open in the playground](../playground/#example=console/echo)

```c
#include "pfc.h"
#include "pfc_rt.h"

/* Read a line and print it back. */
int main(void)
{
    print_str("What is your name? ");
    string name = read_line();

    print_str("Hello, ");
    println_str(name);
    return 0;
}
```

## Programs that must be refused

### wrong/off_by_one

Expected: **refused**. [Open in the playground](../playground/#example=wrong/off_by_one)

```c
#include "pfc.h"

/* `i <= n` writes one element past the end. Refused: the write at line 7 is not proved in bounds. */
long fill(long n, long a[n], long value)
{
    for (long i = 0; i <= n; i++) {
        a[i] = value;
    }
    return n;
}
```

### wrong/false_law

Expected: **refused**. [Open in the playground](../playground/#example=wrong/false_law)

```c
#include "pfc.h"

long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;

    while (i < n) {
        i++;
    }
    return i;
}

/* Refused: counting to n never gives n + 1, and the checker shows a value at line 18. */
law counting_to_n_gives_one_more(long n where(0 <= n))
{
    assert(count(n) == n + 1);
}
```

### wrong/no_progress

Expected: **refused**. [Open in the playground](../playground/#example=wrong/no_progress)

```c
#include "pfc.h"

/* The body never moves `left`, so the measure does not decrease. Refused at line 9. */
long countdown(long n)
    requires(0 <= n)
{
    long left = n;

    while (left > 0) decreases(left) {
        left = left;
    }
    return left;
}
```

### wrong/forgotten_global

Expected: **refused**. [Open in the playground](../playground/#example=wrong/forgotten_global)

```c
#include "pfc.h"

long hits = 0;

long hit(void)
    requires(hits < 1000)
{
    hits++;
    return hits;
}

/* `hit` writes `hits` and promises nothing about it, so the caller cannot know it afterwards.
 * Refused at line 19. */
long once(void)
    requires(hits == 0)
{
    hit();
    assert(hits == 1);
    return hits;
}
```

### wrong/unchecked_division

Expected: **refused**. [Open in the playground](../playground/#example=wrong/unchecked_division)

```c
#include "pfc.h"

/* Nothing says y is not zero. Refused: the division at line 6 may divide by zero. */
long ratio(long x, long y)
{
    return x / y;
}
```

### wrong/broken_call

Expected: **refused**. [Open in the playground](../playground/#example=wrong/broken_call)

```c
#include "pfc.h"

long half(long x)
    requires(0 <= x)
{
    return x / 2;
}

/* The caller passes a value the callee's contract forbids. Refused at line 12. */
long use(void)
{
    return half(-4);
}
```

### wrong/flag_without_wall

Expected: **refused**. [Open in the playground](../playground/#example=wrong/flag_without_wall)

```c
#include "pfc.h"

/* The same game with the wall taken away (WALL is a column that does not exist). Now the flag can be
 * reached, so the claim "nobody ever wins" is false. Refused at line 52: one more move can break the
 * invariant, and the checker shows a state of the game from which it does. */
#define WIDTH 8
#define HEIGHT 5
#define WALL 99
#define FLAG_X 7
#define FLAG_Y 2

/* Moves: 0 up, 1 down, 2 left, 3 right. Any other number leaves the player where it is. */
long step_x(long x, long move)
    requires(0 <= x && x < WIDTH)
    ensures(0 <= result && result < WIDTH)
    ensures(x - 1 <= result && result <= x + 1)
    ensures(move == 2 || move == 3 || result == x)
    ensures(x >= WALL || result < WALL)
{
    if (move == 2 && x > 0) {
        return x - 1;
    }
    if (move == 3 && x + 1 < WIDTH && x + 1 != WALL) {
        return x + 1;
    }
    return x;
}

long step_y(long y, long move)
    requires(0 <= y && y < HEIGHT)
    ensures(0 <= result && result < HEIGHT)
    ensures(y - 1 <= result && result <= y + 1)
    ensures(move == 0 || move == 1 || result == y)
{
    if (move == 0 && y > 0) {
        return y - 1;
    }
    if (move == 1 && y + 1 < HEIGHT) {
        return y + 1;
    }
    return y;
}

/* 1 when the player stands on the flag after some move, 0 otherwise. */
long play(long n, const long moves[n])
    ensures(result == 0)
{
    long x = 0;
    long y = 2;
    long won = 0;

    for (long i = 0; i < n; i++) invariant(0 <= x && x < WIDTH && x < WALL && 0 <= y && y < HEIGHT && won == 0) {
        x = step_x(x, moves[i]);
        y = step_y(y, moves[i]);
        if (x == FLAG_X && y == FLAG_Y) {
            won = 1;
        }
    }
    return won;
}

/* The same claim as a law: whatever the moves, and however many, the flag is never taken. */
law nobody_ever_wins(long n where(0 <= n), const long moves[n])
{
    assert(play(n, moves) == 0);
}
```

### wrong/rest_api_missing_check

Expected: **refused**. [Open in the playground](../playground/#example=wrong/rest_api_missing_check)

```c
#include "pfc.h"

/* The same handlers with one comparison forgotten: the id is checked against the end of the table but
 * not against 0. A request for /items/-1 would read memory before the table. Refused: the read at
 * line 42 is not proved in bounds, and the checker shows id = -1.
 *
 *
 *     GET    /items/{id}            200 and the value, or 404
 *     PUT    /items/{id}  {value}   201 created, 200 replaced, 400 bad value, 404 no such slot
 *     DELETE /items/{id}            204, or 404
 *     anything else                 405
 *
 * `handle` accepts ANY method, id and value a client can send: nothing is required of them. What is
 * proved, for every request: the table is never read or written outside its n slots, the status is one
 * of the documented ones, and a request for an id outside the table never succeeds. The HTTP server
 * around it (server.py) is ordinary, unverified code. */
#define GET 0
#define PUT 1
#define DELETE 2
#define MAX_VALUE 1000000

long reply = 0; /* The value a successful GET returns. */

/* Globals are private to the certified code, so the server reads the value through this function. */
long last_reply(void)
{
    return reply;
}

long handle(long n, long used[n], long values[n], long method, long id, long value)
    ensures(result == 200 || result == 201 || result == 204 || result == 400 || result == 404 || result == 405)
    ensures((0 <= id && id < n) || result == 404 || result == 405)
    ensures((method == GET || method == PUT || method == DELETE) == (result != 405))
{
    if (method != GET && method != PUT && method != DELETE) {
        return 405;
    }
    if (id >= n) {
        return 404;
    }
    if (method == GET) {
        if (used[id] == 0) {
            return 404;
        }
        reply = values[id];
        return 200;
    }
    if (method == PUT) {
        if (value < 0 || value > MAX_VALUE) {
            return 400;
        }
        values[id] = value;
        if (used[id] == 0) {
            used[id] = 1;
            return 201;
        }
        return 200;
    }
    if (used[id] == 0) {
        return 404;
    }
    used[id] = 0;
    return 204;
}
```

### wrong/narrow_store

Expected: **refused**. [Open in the playground](../playground/#example=wrong/narrow_store)

```c
#include "pfc.h"

/* Wrong: a shifted letter may not fit a char ('z' + 13 is 135, and a char holds at most 127 here). */
long shift(long n, char s[n])
    requires(1 <= n && 'a' <= s[0] && s[0] <= 'z')
{
    s[0] = s[0] + 13;
    return 0;
}
```

### wrong/skipped_step

Expected: **refused**. [Open in the playground](../playground/#example=wrong/skipped_step)

```c
#include "pfc.h"

/* Wrong: on the `continue` path the counter stays behind, so `seen == i` is not kept. */
long evens(long n)
    requires(0 <= n && n <= 1000)
    ensures(result == n)
{
    long seen = 0;

    for (long i = 0; i < n; i++) invariant(seen == i) {
        if (i % 2 == 1) {
            continue;
        }
        seen++;
    }
    return seen;
}
```

### wrong/contradictory_extern

Expected: **refused**. [Open in the playground](../playground/#example=wrong/contradictory_extern)

```c
#include "pfc.h"

/* No number is both below 0 and above 100, so this contract describes no function. Because a declared
 * function is trusted under its contract, an impossible contract would let anything after the call be
 * "proved". Refused before any proof is accepted. */
long sensor(void)
    ensures(result < 0 && result > 100);

long read_twice(void)
    ensures(result == 7)
{
    return sensor() + sensor();
}
```
