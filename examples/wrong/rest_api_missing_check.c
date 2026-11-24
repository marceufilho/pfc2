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

