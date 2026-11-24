/* Hand transcription of examples/12_rest_api/api.c. `used` and `values` may overlap, as in PFC2 (no
 * `separated` is written); a caller cannot hold the address of the file's own global, which is stated. */
#define GET 0
#define PUT 1
#define DELETE 2
#define MAX_VALUE 1000000

long reply = 0;

/*@ terminates \false;
    assigns \nothing;
*/
long last_reply(void)
{
    return reply;
}

/*@ requires 0 <= n;
    requires \valid(used + (0 .. n-1));
    requires \valid(values + (0 .. n-1));
    requires \separated(used + (0 .. n-1), &reply);
    requires \separated(values + (0 .. n-1), &reply);
    terminates \false;
    assigns reply, used[0 .. n-1], values[0 .. n-1];
    ensures \result == 200 || \result == 201 || \result == 204 || \result == 400 || \result == 404
            || \result == 405;
    ensures (0 <= id && id < n) || \result == 404 || \result == 405;
    ensures (method == GET || method == PUT || method == DELETE) <==> (\result != 405);
*/
long handle(long n, long used[n], long values[n], long method, long id, long value)
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

/*@ requires 0 <= n;
    requires id < 0;
    requires \valid(used + (0 .. n-1));
    requires \valid(values + (0 .. n-1));
    requires \separated(used + (0 .. n-1), &reply);
    requires \separated(values + (0 .. n-1), &reply);
    terminates \false;
    assigns reply, used[0 .. n-1], values[0 .. n-1];
*/
void negative_id_is_not_found(long n, long used[n], long values[n], long id, long value)
{
    long r = handle(n, used, values, GET, id, value);
    /*@ assert r == 404; */
}
