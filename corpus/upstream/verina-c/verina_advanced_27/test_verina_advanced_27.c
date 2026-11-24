/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_27.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s1[] = {97, 98, 99, 100, 101};
    static const char s2[] = {97, 99, 101};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = longestCommonSubsequence(5, s1, 3, s2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 97 && out[1] == 99 && out[2] == 101);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 97 && out[1] == 98);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 98 && out[1] == 99 && out[2] == 101);
}

static void test_case_1(void)
{
    static const char s1[] = {97, 97, 97, 97};
    static const char s2[] = {98, 98, 97, 97, 97};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = longestCommonSubsequence(4, s1, 5, s2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 97 && out[1] == 97 && out[2] == 97);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 97 && out[1] == 97 && out[2] == 97 && out[3] == 97 && out[4] == 97);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 98);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 97 && out[1] == 97 && out[2] == 97 && out[3] == 98);
}

static void test_case_2(void)
{
    static const char s1[] = {120, 121, 122};
    static const char s2[] = {97, 98, 99};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = longestCommonSubsequence(3, s1, 3, s2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 120);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 121);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
}

static void test_case_3(void)
{
    static const char s1[] = {97, 120, 98, 120, 99};
    static const char s2[] = {97, 98, 120, 99};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = longestCommonSubsequence(5, s1, 4, s2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 97 && out[1] == 98 && out[2] == 120 && out[3] == 99);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 120 && out[2] == 99);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 97 && out[1] == 98 && out[2] == 99 && out[3] == 120);
}

static void test_case_4(void)
{
    static const char s1[] = {65, 71, 71, 84, 65, 66};
    static const char s2[] = {71, 88, 84, 88, 65, 89, 66};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = longestCommonSubsequence(6, s1, 7, s2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 71 && out[1] == 84 && out[2] == 65 && out[3] == 66);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 71 && out[1] == 71 && out[2] == 84 && out[3] == 65 && out[4] == 66);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 65 && out[1] == 71 && out[2] == 71 && out[3] == 84 && out[4] == 65);
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
