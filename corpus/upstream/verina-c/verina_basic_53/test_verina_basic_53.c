/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_53.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = CalSum(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    long found = CalSum(1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    long found = CalSum(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 15);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 16);
    TEST_ASSERT_FALSE(found == 20);
}

static void test_case_3(void)
{
    long found = CalSum(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 55);
    TEST_ASSERT_FALSE(found == 54);
    TEST_ASSERT_FALSE(found == 56);
    TEST_ASSERT_FALSE(found == 50);
}

static void test_case_4(void)
{
    long found = CalSum(20L);
    (void)found;
    TEST_ASSERT_TRUE(found == 210);
    TEST_ASSERT_FALSE(found == 200);
    TEST_ASSERT_FALSE(found == 220);
    TEST_ASSERT_FALSE(found == 205);
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
