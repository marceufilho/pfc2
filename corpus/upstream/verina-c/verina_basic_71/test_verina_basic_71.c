/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_71.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char str1[] = {97, 98, 99};
    static const char str2[] = {97, 98, 100};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = LongestCommonPrefix(3, str1, 3, str2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 97 && out[1] == 98);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
}

static void test_case_1(void)
{
    static const char str1[] = {120, 121, 122};
    static const char str2[] = {120, 121, 122};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = LongestCommonPrefix(3, str1, 3, str2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 120 && out[1] == 121 && out[2] == 122);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 120 && out[1] == 121);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 120 && out[1] == 122);
}

static void test_case_2(void)
{
    static const char str1[] = {119, 111};
    static const char str2[] = {119, 111, 119};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = LongestCommonPrefix(2, str1, 3, str2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 119 && out[1] == 111);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 119);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 111);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 119 && out[1] == 111 && out[2] == 119);
}

static void test_case_3(void)
{
    static const char str1[] = {97, 120};
    static const char str2[] = {98, 121};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = LongestCommonPrefix(2, str1, 2, str2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 98);
}

static void test_case_4(void)
{
    static const char str1[] = {0};
    static const char str2[] = {104, 101, 108, 108, 111};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = LongestCommonPrefix(0, str1, 5, str2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 104);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 101);
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
