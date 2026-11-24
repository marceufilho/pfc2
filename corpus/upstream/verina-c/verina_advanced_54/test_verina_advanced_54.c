/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_54.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {3L, 0L, 1L};
    long found = missingNumber(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    static const long nums[] = {0L, 1L};
    long found = missingNumber(2, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_2(void)
{
    static const long nums[] = {9L, 6L, 4L, 2L, 3L, 5L, 7L, 0L, 1L};
    long found = missingNumber(9, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 8);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_3(void)
{
    static const long nums[] = {0L};
    long found = missingNumber(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const long nums[] = {1L};
    long found = missingNumber(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
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
