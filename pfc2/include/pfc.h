#ifndef PFC_H
#define PFC_H

/* PFC2: C with contracts and laws. The words below are added to the language:
 *
 *     requires(p) ensures(q)         after a function declarator; `result` names the returned value
 *     invariant(i) decreases(e)      between a loop head and its `{`
 *     assert(p)                      a fact proved where it stands
 *     where(p)                       a type: on a parameter or a local
 *     separated(a, b)                inside requires: the two arrays do not overlap
 *     law name(parameters) { ... }   a property proved for every input
 *
 *     long count(long n)
 *         requires(0 <= n)
 *         ensures(result == n)
 *     { ... }
 *
 *     law counting_to_n_gives_n(long n where(0 <= n)) { assert(count(n) == n); }
 *
 * An ordinary compiler sees plain C11: the clauses disappear and a law is an unused static
 * function that is never called or evaluated. The PFC2 checker defines PFC_CHECK, reads the
 * words from the source itself, proves every one and only then emits C. See docs/pfc2/.
 */
#ifdef PFC_CHECK

/* Markers the checker's front end reads; they are never defined and never emitted. */
void __spec_requires(_Bool condition);
void __spec_ensures(_Bool condition);
void __spec_invariant(_Bool condition);
void __spec_assert(_Bool condition);
_Bool __spec_separated(const void *left, long left_len, const void *right, long right_len);

#else

#define requires(condition)
#define ensures(condition)
#define invariant(condition)
#define decreases(measure)
#define where(condition)
#define law __attribute__((unused)) static void
#ifndef assert
/* Proved and erased by the checker; type-checked here but never evaluated. */
#define assert(condition) ((void)sizeof((condition) ? 1 : 0))
#endif
/* Older spellings, written as the first statements of a body. */
#define REQUIRES(condition)
#define ENSURES(condition)
#define INVARIANT(condition)
#define ASSERT(condition)

#endif

#endif
