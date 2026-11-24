# A REST API with proved handlers

`api.c` holds the logic of a small API over a table of items. `server.py` is an ordinary HTTP server around it.

| Request | Answer |
| --- | --- |
| `GET /items/{id}` | `200 {"value": n}`, or `404` |
| `PUT /items/{id}` with `{"value": n}` | `201` created, `200` replaced, `400` when `n` is outside 0..1000000, `404` when there is no such slot |
| `DELETE /items/{id}` | `204`, or `404` |
| any other method | `405` |

## What is proved

`handle(n, used, values, method, id, value)` takes any three numbers a client can send; nothing is required of
them. For every such request PFC2 proves that:

- the table is never read or written outside its `n` slots (7 accesses, no bounds check left in the emitted C);
- the status is one of 200, 201, 204, 400, 404, 405;
- a request whose id is outside the table gets 404 or 405, never a success;
- 405 is returned exactly for the methods that are not GET, PUT or DELETE;
- the law `negative_id_is_not_found`: a GET with a negative id is always 404.

```console
$ uv run pfc2 check examples/12_rest_api/api.c
api.c: certified (full)
  obligations proved: 38 of 38 (Z3 5.3.3.0)
  bounds/division checks removed: 7 of 7
```

## The same API with a bug

`examples/wrong/rest_api_missing_check.c` forgets one comparison: the id is checked against the end of the table
but not against 0. That is the classic way an API reads memory it should not.

```console
$ uv run pfc2 check examples/wrong/rest_api_missing_check.c
rest_api_missing_check.c: not certified (full): 12 obligation(s) not proved
  rest_api_missing_check.c:42:13: this index may be outside the array [failed]
      cannot prove: ((0 <= id) && (id < n))
      for example:  reply = 0, n = 0, method = 0, id = -1, value = 0
```

The checker names the request that breaks it (`id = -1`), and releases no C.

## Run it

```console
$ uv run pfc2 build examples/12_rest_api/api.c --output build/api
$ clang-19 -std=c11 -O2 -shared -fPIC build/api/api.c -o build/api/libapi.so
$ uv run python examples/12_rest_api/server.py build/api/libapi.so --port 8080
$ curl -X PUT -d '{"value": 5}' http://127.0.0.1:8080/items/2     # {"status": 201}
$ curl http://127.0.0.1:8080/items/2                              # {"value": 5}
$ curl -i http://127.0.0.1:8080/items/-1                          # 404
```

## What is not proved

`server.py`, Python's HTTP library, the JSON parsing and the operating system. The server decides what counts as
a well-formed URL and body before the certified code sees three numbers; a bug there is outside the proof.
`tests/test_rest_api.py` runs 17 requests over real HTTP against the certified library and compares each answer
with the table above.
