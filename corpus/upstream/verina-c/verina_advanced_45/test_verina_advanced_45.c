/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_45.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {1L, -2L, 3L, 4L, -1L};
    long found = maxSubarraySum(5, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_1(void)
{
    static const long xs[] = {-2L, -3L, -1L, -5L};
    long found = maxSubarraySum(4, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const long xs[] = {5L, -1L, 2L, -1L, 3L};
    long found = maxSubarraySum(5, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 8);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_3(void)
{
    static const long xs[] = {0};
    long found = maxSubarraySum(0, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long xs[] = {4L, -1L, -2L, 1L, 5L};
    long found = maxSubarraySum(5, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 8);
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
