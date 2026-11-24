/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_34.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {10L, 9L, 2L, 5L, 3L, 7L, 101L, 18L};
    long found = longestIncreasingSubsequence(8, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 100);
}

static void test_case_1(void)
{
    static const long nums[] = {0L, 1L, 0L, 3L, 2L, 3L};
    long found = longestIncreasingSubsequence(6, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 100);
}

static void test_case_2(void)
{
    static const long nums[] = {7L, 7L, 7L, 7L, 7L, 7L, 7L};
    long found = longestIncreasingSubsequence(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_3(void)
{
    static const long nums[] = {1L, 3L, 2L, 4L};
    long found = longestIncreasingSubsequence(4, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_4(void)
{
    static const long nums[] = {10L};
    long found = longestIncreasingSubsequence(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
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
