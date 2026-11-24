/* PFC2 console runtime. Ordinary, unverified C: the boundary between a certified program and the world.
 * A string is passed as a long holding the address of a NUL-terminated array of char (LP64). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

_Static_assert(sizeof(long) == sizeof(char *), "pfc_rt keeps a string address in a long");

#define PFC_RT_LINE 4096

long print_int(long value) { printf("%ld", value); return 0; }
long print_str(long text) { fputs((const char *)text, stdout); return 0; }
long println(void) { putchar('\n'); return 0; }
long println_str(long text) { puts((const char *)text); return 0; }

/* One line without its newline; the empty string at end of input. Never freed: a program is short-lived. */
long read_line(void)
{
    char buffer[PFC_RT_LINE];
    char *line;
    size_t length;

    fflush(stdout);
    if (fgets(buffer, sizeof buffer, stdin) == NULL) {
        buffer[0] = '\0';
    }
    length = strcspn(buffer, "\r\n");
    line = malloc(length + 1);
    if (line == NULL) {
        abort();
    }
    memcpy(line, buffer, length);
    line[length] = '\0';
    return (long)line;
}

/* One line read as a decimal integer; 0 when the line is not one or does not fit a long. */
long read_int(void)
{
    char buffer[PFC_RT_LINE];
    char *end;
    long value;

    fflush(stdout);
    if (fgets(buffer, sizeof buffer, stdin) == NULL) {
        return 0;
    }
    value = strtol(buffer, &end, 10);
    if (end == buffer || (*end != '\0' && *end != '\n' && *end != '\r')) {
        return 0;
    }
    return value;
}

long str_eq(long left, long right) { return strcmp((const char *)left, (const char *)right) == 0; }
