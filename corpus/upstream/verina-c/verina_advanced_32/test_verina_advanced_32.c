/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_32.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long numbers[] = {10L, 22L, 9L, 33L, 21L, 50L, 41L, 60L};
    long found = longestIncreasingSubsequence(8, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_1(void)
{
    static const long numbers[] = {3L, 10L, 2L, 1L, 20L};
    long found = longestIncreasingSubsequence(5, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    static const long numbers[] = {50L, 3L, 10L, 7L, 40L, 80L};
    long found = longestIncreasingSubsequence(6, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_3(void)
{
    static const long numbers[] = {10L, 9L, 8L, 7L, 6L, 5L, 4L, 3L, 2L, 1L};
    long found = longestIncreasingSubsequence(10, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_4(void)
{
    static const long numbers[] = {1L, 2L, 3L, 4L, 5L};
    long found = longestIncreasingSubsequence(5, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_5(void)
{
    static const long numbers[] = {0};
    long found = longestIncreasingSubsequence(0, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_6(void)
{
    static const long numbers[] = {5L};
    long found = longestIncreasingSubsequence(1, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_7(void)
{
    static const long numbers[] = {5L, 5L, 5L, 5L};
    long found = longestIncreasingSubsequence(4, numbers);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 4);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    RUN_TEST(test_case_3);
    RUN_TEST(test_case_4);
    RUN_TEST(test_case_5);
    RUN_TEST(test_case_6);
    RUN_TEST(test_case_7);
    return UNITY_END();
}
