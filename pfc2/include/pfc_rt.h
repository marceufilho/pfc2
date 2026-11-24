#ifndef PFC_RT_H
#define PFC_RT_H

/* PFC2 console runtime: the functions below are implemented in pfc2/runtime/pfc_rt.c, ordinary C that
 * is not verified. A program calls them under the contracts written here; the checker lists every one
 * of them as an unverified boundary. A `string` is opaque to the proofs: it can be stored, passed,
 * printed and compared, and nothing is proved about its characters.
 *
 *     print_int(n)  print_str(s)  println()  println_str(s)   write to standard output; return 0
 *     read_int()                                              one line as an integer; 0 if it is not one
 *     read_line()                                             one line without its newline
 *     str_eq(a, b)                                            1 when the two strings have the same characters
 */
#ifdef PFC_CHECK

#define string long
long print_int(long value);
long print_str(string text);
long println(void);
long println_str(string text);
long read_int(void);
string read_line(void);
long str_eq(string left, string right) ensures(result == 0 || result == 1);

#else

typedef const char *string;
long print_int(long value);
long (print_str)(long text);
long println(void);
long (println_str)(long text);
long read_int(void);
long (read_line)(void);
long (str_eq)(long left, long right);
/* The checked program holds a string as a long (the address). These keep the same source valid C. */
#define print_str(text) (print_str)((long)(text))
#define println_str(text) (println_str)((long)(text))
#define read_line() ((string)(read_line)())
#define str_eq(left, right) (str_eq)((long)(left), (long)(right))

#endif

#endif
