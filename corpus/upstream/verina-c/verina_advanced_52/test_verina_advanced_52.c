/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_52.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {3L, 1L, 5L, 4L, 2L};
    long found = minOperations(5, nums, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_1(void)
{
    static const long nums[] = {3L, 1L, 5L, 4L, 2L};
    long found = minOperations(5, nums, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const long nums[] = {3L, 2L, 5L, 3L, 1L};
    long found = minOperations(5, nums, 3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_3(void)
{
    static const long nums[] = {5L, 4L, 3L, 2L, 1L};
    long found = minOperations(5, nums, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_4(void)
{
    static const long nums[] = {5L, 4L, 1L, 2L, 3L};
    long found = minOperations(5, nums, 3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_5(void)
{
    static const long nums[] = {1L, 3L, 2L, 2L, 1L};
    long found = minOperations(5, nums, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_6(void)
{
    static const long nums[] = {10L, 1L, 20L, 2L};
    long found = minOperations(4, nums, 2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_7(void)
{
    static const long nums[] = {1L, 2L, 3L};
    long found = minOperations(3, nums, 0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
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
