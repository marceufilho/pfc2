/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_42.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long prices[] = {7L, 1L, 5L, 3L, 6L, 4L};
    long found = maxProfit(6, prices);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_1(void)
{
    static const long prices[] = {7L, 6L, 4L, 3L, 1L};
    long found = maxProfit(5, prices);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_2(void)
{
    static const long prices[] = {2L, 4L, 1L};
    long found = maxProfit(3, prices);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    static const long prices[] = {1L, 2L};
    long found = maxProfit(2, prices);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const long prices[] = {0};
    long found = maxProfit(0, prices);
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
