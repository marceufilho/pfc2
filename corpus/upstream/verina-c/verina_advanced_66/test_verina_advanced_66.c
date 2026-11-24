/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_66.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char words_str[] = {116, 104, 101, 32, 115, 107, 121, 32, 105, 115, 32, 98, 108, 117, 101};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = reverseWords(15, words_str, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 15 && out[0] == 98 && out[1] == 108 && out[2] == 117 && out[3] == 101 && out[4] == 32 && out[5] == 105 && out[6] == 115 && out[7] == 32 && out[8] == 115 && out[9] == 107 && out[10] == 121 && out[11] == 32 && out[12] == 116 && out[13] == 104 && out[14] == 101);
    TEST_ASSERT_FALSE(found == 15 && out[0] == 116 && out[1] == 104 && out[2] == 101 && out[3] == 32 && out[4] == 115 && out[5] == 107 && out[6] == 121 && out[7] == 32 && out[8] == 105 && out[9] == 115 && out[10] == 32 && out[11] == 98 && out[12] == 108 && out[13] == 117 && out[14] == 101);
    TEST_ASSERT_FALSE(found == 15 && out[0] == 115 && out[1] == 107 && out[2] == 121 && out[3] == 32 && out[4] == 116 && out[5] == 104 && out[6] == 101 && out[7] == 32 && out[8] == 98 && out[9] == 108 && out[10] == 117 && out[11] == 101 && out[12] == 32 && out[13] == 105 && out[14] == 115);
}

static void test_case_1(void)
{
    static const char words_str[] = {32, 32, 104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 32, 32};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = reverseWords(15, words_str, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 11 && out[0] == 119 && out[1] == 111 && out[2] == 114 && out[3] == 108 && out[4] == 100 && out[5] == 32 && out[6] == 104 && out[7] == 101 && out[8] == 108 && out[9] == 108 && out[10] == 111);
    TEST_ASSERT_FALSE(found == 11 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 32 && out[6] == 119 && out[7] == 111 && out[8] == 114 && out[9] == 108 && out[10] == 100);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 119 && out[1] == 111 && out[2] == 114 && out[3] == 108 && out[4] == 100 && out[5] == 104 && out[6] == 101 && out[7] == 108 && out[8] == 108 && out[9] == 111);
}

static void test_case_2(void)
{
    static const char words_str[] = {97, 32, 103, 111, 111, 100, 32, 32, 32, 101, 120, 97, 109, 112, 108, 101};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = reverseWords(16, words_str, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 14 && out[0] == 101 && out[1] == 120 && out[2] == 97 && out[3] == 109 && out[4] == 112 && out[5] == 108 && out[6] == 101 && out[7] == 32 && out[8] == 103 && out[9] == 111 && out[10] == 111 && out[11] == 100 && out[12] == 32 && out[13] == 97);
    TEST_ASSERT_FALSE(found == 14 && out[0] == 97 && out[1] == 32 && out[2] == 103 && out[3] == 111 && out[4] == 111 && out[5] == 100 && out[6] == 32 && out[7] == 101 && out[8] == 120 && out[9] == 97 && out[10] == 109 && out[11] == 112 && out[12] == 108 && out[13] == 101);
    TEST_ASSERT_FALSE(found == 14 && out[0] == 101 && out[1] == 120 && out[2] == 97 && out[3] == 109 && out[4] == 112 && out[5] == 108 && out[6] == 101 && out[7] == 32 && out[8] == 97 && out[9] == 32 && out[10] == 103 && out[11] == 111 && out[12] == 111 && out[13] == 100);
}

static void test_case_3(void)
{
    static const char words_str[] = {32, 32, 66, 111, 98, 32, 32, 32, 32, 76, 111, 118, 101, 115, 32, 32, 65, 108, 105, 99, 101, 32, 32, 32};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = reverseWords(24, words_str, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 15 && out[0] == 65 && out[1] == 108 && out[2] == 105 && out[3] == 99 && out[4] == 101 && out[5] == 32 && out[6] == 76 && out[7] == 111 && out[8] == 118 && out[9] == 101 && out[10] == 115 && out[11] == 32 && out[12] == 66 && out[13] == 111 && out[14] == 98);
    TEST_ASSERT_FALSE(found == 15 && out[0] == 66 && out[1] == 111 && out[2] == 98 && out[3] == 32 && out[4] == 76 && out[5] == 111 && out[6] == 118 && out[7] == 101 && out[8] == 115 && out[9] == 32 && out[10] == 65 && out[11] == 108 && out[12] == 105 && out[13] == 99 && out[14] == 101);
    TEST_ASSERT_FALSE(found == 16 && out[0] == 65 && out[1] == 108 && out[2] == 105 && out[3] == 99 && out[4] == 101 && out[5] == 32 && out[6] == 76 && out[7] == 111 && out[8] == 118 && out[9] == 101 && out[10] == 115 && out[11] == 32 && out[12] == 66 && out[13] == 111 && out[14] == 98 && out[15] == 32);
}

static void test_case_4(void)
{
    static const char words_str[] = {116, 104, 105, 115, 32, 108, 97, 98, 32, 105, 115, 32, 105, 110, 116, 101, 114, 101, 115, 116, 105, 110, 103};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = reverseWords(23, words_str, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 23 && out[0] == 105 && out[1] == 110 && out[2] == 116 && out[3] == 101 && out[4] == 114 && out[5] == 101 && out[6] == 115 && out[7] == 116 && out[8] == 105 && out[9] == 110 && out[10] == 103 && out[11] == 32 && out[12] == 105 && out[13] == 115 && out[14] == 32 && out[15] == 108 && out[16] == 97 && out[17] == 98 && out[18] == 32 && out[19] == 116 && out[20] == 104 && out[21] == 105 && out[22] == 115);
    TEST_ASSERT_FALSE(found == 23 && out[0] == 103 && out[1] == 110 && out[2] == 105 && out[3] == 116 && out[4] == 115 && out[5] == 101 && out[6] == 114 && out[7] == 101 && out[8] == 116 && out[9] == 110 && out[10] == 105 && out[11] == 32 && out[12] == 115 && out[13] == 105 && out[14] == 32 && out[15] == 98 && out[16] == 97 && out[17] == 108 && out[18] == 32 && out[19] == 115 && out[20] == 105 && out[21] == 104 && out[22] == 116);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    RUN_TEST(test_case_3);
    RUN_TEST(test_case_4);
    return UNITY_END();
}
