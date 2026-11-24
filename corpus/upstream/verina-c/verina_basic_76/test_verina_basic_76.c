/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_76.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = myMin(3L, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_1(void)
{
    long found = myMin(10L, 7L);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 17);
}

static void test_case_2(void)
{
    long found = myMin(4L, 4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_3(void)
{
    long found = myMin(-5L, 0L);
    (void)found;
    TEST_ASSERT_TRUE(found == -5);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -4);
}

static void test_case_4(void)
{
    long found = myMin(0L, -10L);
    (void)found;
    TEST_ASSERT_TRUE(found == -10);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -8);
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
