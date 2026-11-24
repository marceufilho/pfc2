/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_41.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = maxOfThree(3L, 2L, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_1(void)
{
    long found = maxOfThree(5L, 5L, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_2(void)
{
    long found = maxOfThree(10L, 20L, 15L);
    (void)found;
    TEST_ASSERT_TRUE(found == 20);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 15);
}

static void test_case_3(void)
{
    long found = maxOfThree(-1L, -2L, -3L);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -3);
}

static void test_case_4(void)
{
    long found = maxOfThree(0L, -10L, -5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -5);
    TEST_ASSERT_FALSE(found == -10);
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
