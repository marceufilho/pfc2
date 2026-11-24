/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_6.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = minOfThree(3L, 2L, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    long found = minOfThree(5L, 5L, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_2(void)
{
    long found = minOfThree(10L, 20L, 15L);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == 15);
    TEST_ASSERT_FALSE(found == 20);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_3(void)
{
    long found = minOfThree(-1L, 2L, 3L);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    long found = minOfThree(2L, -3L, 4L);
    (void)found;
    TEST_ASSERT_TRUE(found == -3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_5(void)
{
    long found = minOfThree(2L, 3L, -5L);
    (void)found;
    TEST_ASSERT_TRUE(found == -5);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_6(void)
{
    long found = minOfThree(0L, 0L, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_7(void)
{
    long found = minOfThree(0L, -1L, 1L);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_8(void)
{
    long found = minOfThree(-5L, -2L, -3L);
    (void)found;
    TEST_ASSERT_TRUE(found == -5);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -3);
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
    RUN_TEST(test_case_5);
    RUN_TEST(test_case_6);
    RUN_TEST(test_case_7);
    RUN_TEST(test_case_8);
    return UNITY_END();
}
