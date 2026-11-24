/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_35.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {3L, 2L, 3L};
    long found = majorityElement(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_1(void)
{
    static const long nums[] = {2L, 2L, 1L, 1L, 1L, 2L, 2L};
    long found = majorityElement(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_2(void)
{
    static const long nums[] = {1L, 1L, 1L, 2L, 3L, 1L};
    long found = majorityElement(6, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_3(void)
{
    static const long nums[] = {0L, 0L, 0L, 0L};
    long found = majorityElement(4, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long nums[] = {7L};
    long found = majorityElement(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
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
