/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_36.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 46, 32, 72, 111, 119, 32, 97, 114, 101, 32, 121, 111, 117, 63};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = replaceWithColon(26, s, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 26 && out[0] == 72 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 58 && out[6] == 58 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 58 && out[13] == 58 && out[14] == 72 && out[15] == 111 && out[16] == 119 && out[17] == 58 && out[18] == 97 && out[19] == 114 && out[20] == 101 && out[21] == 58 && out[22] == 121 && out[23] == 111 && out[24] == 117 && out[25] == 63);
    TEST_ASSERT_FALSE(found == 24 && out[0] == 72 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 119 && out[7] == 111 && out[8] == 114 && out[9] == 108 && out[10] == 100 && out[11] == 44 && out[12] == 72 && out[13] == 111 && out[14] == 119 && out[15] == 44 && out[16] == 97 && out[17] == 114 && out[18] == 101 && out[19] == 44 && out[20] == 121 && out[21] == 111 && out[22] == 117 && out[23] == 63);
    TEST_ASSERT_FALSE(found == 28 && out[0] == 72 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 58 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 58 && out[13] == 32 && out[14] == 72 && out[15] == 111 && out[16] == 119 && out[17] == 58 && out[18] == 32 && out[19] == 97 && out[20] == 114 && out[21] == 101 && out[22] == 58 && out[23] == 32 && out[24] == 121 && out[25] == 111 && out[26] == 117 && out[27] == 63);
}

static void test_case_1(void)
{
    static const char s[] = {78, 111, 45, 99, 104, 97, 110, 103, 101, 115, 33};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = replaceWithColon(11, s, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 11 && out[0] == 78 && out[1] == 111 && out[2] == 45 && out[3] == 99 && out[4] == 104 && out[5] == 97 && out[6] == 110 && out[7] == 103 && out[8] == 101 && out[9] == 115 && out[10] == 33);
    TEST_ASSERT_FALSE(found == 11 && out[0] == 78 && out[1] == 111 && out[2] == 32 && out[3] == 99 && out[4] == 104 && out[5] == 97 && out[6] == 110 && out[7] == 103 && out[8] == 101 && out[9] == 115 && out[10] == 33);
}

static void test_case_2(void)
{
    static const char s[] = {44, 46, 32};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = replaceWithColon(3, s, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 58 && out[1] == 58 && out[2] == 58);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 58 && out[1] == 58);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 59 && out[1] == 58 && out[2] == 59);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 58 && out[1] == 58 && out[2] == 58 && out[3] == 32);
}

static void test_case_3(void)
{
    static const char s[] = {0};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = replaceWithColon(0, s, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 32);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    RUN_TEST(test_case_3);
    return UNITY_END();
}
