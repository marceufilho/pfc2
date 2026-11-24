/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_28.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {100L, 4L, 200L, 1L, 3L, 2L};
    long found = longestConsecutive(6, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_1(void)
{
    static const long nums[] = {0L, 3L, 7L, 2L, 5L, 8L, 4L, 6L, 1L};
    long found = longestConsecutive(9, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_2(void)
{
    static const long nums[] = {1L, 2L, 0L};
    long found = longestConsecutive(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_3(void)
{
    static const long nums[] = {0};
    long found = longestConsecutive(0, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long nums[] = {10L};
    long found = longestConsecutive(1, nums);
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
