/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_37.h"

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
    static const long nums[] = {1L};
    long found = majorityElement(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long nums[] = {4L, 4L, 4L, 4L, 4L, 2L, 2L, 3L, 3L};
    long found = majorityElement(9, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_4(void)
{
    static const long nums[] = {9L, 8L, 9L, 9L, 7L, 9L, 6L, 9L, 9L};
    long found = majorityElement(9, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_5(void)
{
    static const long nums[] = {0L, 0L, 0L, 0L, 1L};
    long found = majorityElement(5, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_6(void)
{
    static const long nums[] = {100000L, 100000L, 100000L, 100000L, -100000L};
    long found = majorityElement(5, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 100000);
    TEST_ASSERT_FALSE(found == -100000);
}

static void test_case_7(void)
{
    static const long nums[] = {-1L, -1L, -1L, -1L, 0L, 1L, 2L};
    long found = majorityElement(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_8(void)
{
    static const long nums[] = {5L, 5L, 5L, 5L, 5L, 5L, 5L};
    long found = majorityElement(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_9(void)
{
    static const long nums[] = {1L, 2L, 3L, 3L, 3L, 3L, 3L};
    long found = majorityElement(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
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
    RUN_TEST(test_case_6);
    RUN_TEST(test_case_7);
    RUN_TEST(test_case_8);
    RUN_TEST(test_case_9);
    return UNITY_END();
}
