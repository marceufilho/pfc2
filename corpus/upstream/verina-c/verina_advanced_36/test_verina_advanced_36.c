/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_36.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {3L, 3L, 4L, 2L, 3L, 3L, 3L};
    long found = majorityElement(7, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_1(void)
{
    static const long xs[] = {1L, 1L, 2L, 1L, 3L, 1L, 1L};
    long found = majorityElement(7, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const long xs[] = {2L, 2L, 2L, 1L, 1L};
    long found = majorityElement(5, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    static const long xs[] = {9L, 9L, 9L, 9L, 1L, 2L, 3L};
    long found = majorityElement(7, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_4(void)
{
    static const long xs[] = {5L, 5L, 5L, 5L, 5L, 6L, 7L};
    long found = majorityElement(7, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 7);
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
