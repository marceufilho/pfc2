/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_4.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {5L, 2L, 8L, 6L, 3L, 6L, 9L, 7L};
    long found = LongestIncreasingSubsequence(8, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    static const long a[] = {3L, 1L, 2L, 1L, 0L};
    long found = LongestIncreasingSubsequence(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const long a[] = {2L, 3L, -2L, -1L, 7L, 19L, 3L, 6L, -4L, 6L, -7L, 0L, 9L, 12L, 10L};
    long found = LongestIncreasingSubsequence(15, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_3(void)
{
    static const long a[] = {5L, -5L, -3L, 2L, 4L, 1L, 0L, -1L, 3L, 2L, 0L};
    long found = LongestIncreasingSubsequence(11, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_4(void)
{
    static const long a[] = {1L, 7L, 23L, 14L, -4L, 21L, 8L, 2L, -1L, 9L, 12L, 2L};
    long found = LongestIncreasingSubsequence(12, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_5(void)
{
    static const long a[] = {0};
    long found = LongestIncreasingSubsequence(0, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
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
    return UNITY_END();
}
