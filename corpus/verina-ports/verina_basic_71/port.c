#include "pfc.h"

/* Verina verina_basic_71: longest common prefix of two character lists, written to out; returns its length. */
long LongestCommonPrefix(long str1_len, const char str1[str1_len], long str2_len, const char str2[str2_len],
                         long out_cap, char out[out_cap])
    requires(out_cap >= str1_len)
{
    long length = 0;

    while (length < str1_len && length < str2_len && str1[length] == str2[length]) {
        out[length] = str1[length];
        length++;
    }
    return length;
}
