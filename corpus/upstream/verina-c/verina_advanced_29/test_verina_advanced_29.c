/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_29.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {1L, 2L, 3L, 1L, 2L, 3L, 1L, 2L};
    long found = longestGoodSubarray(8, nums, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_1(void)
{
    static const long nums[] = {1L, 2L, 1L, 2L, 1L, 2L, 1L, 2L};
    long found = longestGoodSubarray(8, nums, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_2(void)
{
    static const long nums[] = {5L, 5L, 5L, 5L, 5L, 5L, 5L};
    long found = longestGoodSubarray(7, nums, 4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_3(void)
{
    static const long nums[] = {1L};
    long found = longestGoodSubarray(1, nums, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_4(void)
{
    static const long nums[] = {2L, 2L, 1L, 1L, 3L};
    long found = longestGoodSubarray(5, nums, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
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
