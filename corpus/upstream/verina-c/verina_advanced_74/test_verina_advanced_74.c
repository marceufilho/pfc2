/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_74.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {1L};
    long found = solution(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_1(void)
{
    static const long nums[] = {1L, 1L, 1L};
    long found = solution(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const long nums[] = {1L, 2L, 1L};
    long found = solution(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 15);
    TEST_ASSERT_FALSE(found == 12);
}

static void test_case_3(void)
{
    static const long nums[] = {1L, 2L, 3L, 4L};
    long found = solution(4, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 50);
}

static void test_case_4(void)
{
    static const long nums[] = {1L, 2L, 2L, 3L, 1L};
    long found = solution(5, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 62);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
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
