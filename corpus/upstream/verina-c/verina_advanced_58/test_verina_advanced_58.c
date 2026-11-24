/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_58.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = nthUglyNumber(1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_1(void)
{
    long found = nthUglyNumber(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 12);
    TEST_ASSERT_FALSE(found == 13);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 15);
}

static void test_case_2(void)
{
    long found = nthUglyNumber(15L);
    (void)found;
    TEST_ASSERT_TRUE(found == 24);
    TEST_ASSERT_FALSE(found == 20);
    TEST_ASSERT_FALSE(found == 25);
}

static void test_case_3(void)
{
    long found = nthUglyNumber(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_4(void)
{
    long found = nthUglyNumber(7L);
    (void)found;
    TEST_ASSERT_TRUE(found == 8);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 10);
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
