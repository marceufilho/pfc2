/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_75.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long sequence[] = {10L, -4L, 3L, 1L, 5L, 6L, -35L, 12L, 21L, -1L};
    long found = task_code(10, sequence);
    (void)found;
    TEST_ASSERT_TRUE(found == 33);
    TEST_ASSERT_FALSE(found == 32);
    TEST_ASSERT_FALSE(found == 34);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const long sequence[] = {2L, 1L, -4L, 3L, 4L, -4L, 6L, 5L, -5L, 1L};
    long found = task_code(10, sequence);
    (void)found;
    TEST_ASSERT_TRUE(found == 14);
    TEST_ASSERT_FALSE(found == 13);
    TEST_ASSERT_FALSE(found == 15);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const long sequence[] = {-1L, -2L, -3L, -4L, -5L};
    long found = task_code(5, sequence);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    static const long sequence[] = {7L};
    long found = task_code(1, sequence);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -7);
}

static void test_case_4(void)
{
    static const long sequence[] = {1L, 2L, 3L, 4L, 5L};
    long found = task_code(5, sequence);
    (void)found;
    TEST_ASSERT_TRUE(found == 15);
    TEST_ASSERT_FALSE(found == 14);
    TEST_ASSERT_FALSE(found == 16);
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
