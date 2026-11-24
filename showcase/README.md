# Showcase

Five small programs the site is built around. `showcase.json` holds the expectation of each, written by hand.

- `midpoint/`: the middle of a range. `(lo + hi) / 2` is refused with the two numbers that overflow;
  `lo + (hi - lo) / 2` is certified.
- `lock/`: a four-key lock. Two laws: the combination opens it, and nothing else does. The loop invariant of
  `lock.c` was proposed by a language model and admitted by the checker at the first attempt
  (`model-proof.json` is the proof file of that run); `lock_without_invariant.c` is the same program before it,
  and is refused.
- `wrong/lock_copy_paste.c`: the lock with a slip that tests do not notice; refused with a fourth key that
  should not open it.

```console
$ uv run pfc2 check showcase/lock/lock.c
$ uv run pfc2 check showcase/midpoint/midpoint_wrong.c
```
