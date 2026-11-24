/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_50.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = Abs(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == -5);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_1(void)
{
    long found = Abs(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -5);
}

static void test_case_2(void)
{
    long found = Abs(-5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == -5);
    TEST_ASSERT_FALSE(found == -10);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    long found = Abs(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == -10);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_4(void)
{
    long found = Abs(-10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == -10);
    TEST_ASSERT_FALSE(found == -1);
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
