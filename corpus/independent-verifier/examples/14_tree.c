/* Hand transcription of examples/14_tree/tree.c. */
#define LAST 1000000

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
    ensures \result == 2 * i + 1;
*/
long left(long i)
{
    return 2 * i + 1;
}

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
    ensures \result == 2 * i + 2;
*/
long right(long i)
{
    return 2 * i + 2;
}

/*@ requires 1 <= i && i <= 2000002;
    terminates \false;
    assigns \nothing;
    ensures \result == (i - 1) / 2;
*/
long parent(long i)
{
    return (i - 1) / 2;
}

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
    ensures 0 <= \result && \result <= i;
*/
long depth(long i)
{
    long node = i;
    long steps = 0;
    /*@ loop invariant 0 <= node && 0 <= steps && steps + node <= i;
        loop assigns node, steps;
        loop variant node;
    */
    while (node > 0) {
        node = parent(node);
        steps++;
    }
    return steps;
}

/*@ requires 0 <= n;
    requires \valid_read(tree + (0 .. n-1));
    requires 0 <= i && i < n && n <= LAST;
    terminates \false;
    assigns \nothing;
*/
long path_max(long n, const long tree[n], long i)
{
    long node = i;
    long best = tree[i];
    /*@ loop invariant 0 <= node && node <= i;
        loop assigns node, best;
        loop variant node;
    */
    while (node > 0) {
        node = parent(node);
        if (tree[node] > best) {
            best = tree[node];
        }
    }
    return best;
}

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
*/
void the_parent_of_a_left_child_is_the_node(long i)
{
    long child = left(i);
    long up = parent(child);
    /*@ assert up == i; */
}

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
*/
void the_parent_of_a_right_child_is_the_node(long i)
{
    long child = right(i);
    long up = parent(child);
    /*@ assert up == i; */
}

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
*/
void children_are_adjacent_and_below(long i)
{
    long l = left(i);
    long r = right(i);
    /*@ assert r == l + 1; */
    /*@ assert i < l; */
}

/*@ requires 0 <= i && i <= LAST;
    requires 0 <= j && j <= LAST;
    terminates \false;
    assigns \nothing;
*/
void left_children_do_not_collide(long i, long j)
{
    long one = left(i);
    long other = left(j);
    /*@ assert one != other || i == j; */
}

/*@ requires 1 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
*/
void every_node_is_a_child_of_its_parent(long i)
{
    long up = parent(i);
    long first = left(up);
    long second = right(up);
    /*@ assert up < i; */
    /*@ assert first == i || second == i; */
}

/*@ requires 0 <= i && i <= LAST;
    terminates \false;
    assigns \nothing;
*/
void the_walk_to_the_root_is_bounded(long i)
{
    long d = depth(i);
    /*@ assert d <= i; */
}
