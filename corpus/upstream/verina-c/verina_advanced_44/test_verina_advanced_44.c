/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_44.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long arr[] = {1L, 2L, 3L, 4L, 5L};
    long found = maxSubarraySumDivisibleByK(5, arr, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 14);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 15);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_1(void)
{
    static const long arr[] = {1L, -2L, 3L, -4L, 5L};
    long found = maxSubarraySumDivisibleByK(5, arr, 3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const long arr[] = {0};
    long found = maxSubarraySumDivisibleByK(0, arr, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_3(void)
{
    static const long arr[] = {1L, 2L, 3L, 4L};
    long found = maxSubarraySumDivisibleByK(4, arr, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_4(void)
{
    static const long arr[] = {-2L, 7L, 1L, 3L};
    long found = maxSubarraySumDivisibleByK(4, arr, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 11);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_5(void)
{
    static const long arr[] = {-100L, 0L, 1L};
    long found = maxSubarraySumDivisibleByK(3, arr, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -99);
}

static void test_case_6(void)
{
    static const long arr[] = {1999L, 1L, -1023L, 12351L, -9999L};
    long found = maxSubarraySumDivisibleByK(5, arr, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 13328);
    TEST_ASSERT_FALSE(found == 1999);
    TEST_ASSERT_FALSE(found == 12351);
    TEST_ASSERT_FALSE(found == 3329);
    TEST_ASSERT_FALSE(found == 2352);
}

static void test_case_7(void)
{
    static const long arr[] = {-5L, -5L};
    long found = maxSubarraySumDivisibleByK(2, arr, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == -10);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -6);
    TEST_ASSERT_FALSE(found == -5);
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
