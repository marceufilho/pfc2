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
