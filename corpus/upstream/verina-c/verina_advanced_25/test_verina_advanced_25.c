/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_25.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {10L, 9L, 2L, 5L, 3L, 7L, 101L, 18L};
    long found = lengthOfLIS(8, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_1(void)
{
    static const long nums[] = {0L, 1L, 0L, 3L, 2L, 3L};
    long found = lengthOfLIS(6, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    static const long nums[] = {7L, 7L, 7L, 7L, 7L, 7L, 7L};
    long found = lengthOfLIS(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_3(void)
{
    static const long nums[] = {0};
    long found = lengthOfLIS(0, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long nums[] = {4L, 10L, 4L, 3L, 8L, 9L};
    long found = lengthOfLIS(6, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_5(void)
{
    static const long nums[] = {1L, 3L, 6L, 7L, 9L, 4L, 10L, 5L, 6L};
    long found = lengthOfLIS(9, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_6(void)
{
    static const long nums[] = {10L, 22L, 9L, 33L, 21L, 50L, 41L, 60L, 80L};
    long found = lengthOfLIS(9, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_7(void)
{
    static const long nums[] = {0L, 8L, 4L, 12L, 2L, 10L, 6L, 14L, 1L, 9L, 5L, 13L, 3L, 11L, 7L, 15L};
    long found = lengthOfLIS(16, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 16);
}

static void test_case_8(void)
{
    static const long nums[] = {-2L, -1L};
    long found = lengthOfLIS(2, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
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
    RUN_TEST(test_case_5);
    RUN_TEST(test_case_6);
    RUN_TEST(test_case_7);
    RUN_TEST(test_case_8);
    return UNITY_END();
}
