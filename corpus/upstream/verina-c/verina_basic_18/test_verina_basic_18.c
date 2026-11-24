/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_18.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = sumOfDigits(12345L);
    (void)found;
    TEST_ASSERT_TRUE(found == 15);
    TEST_ASSERT_FALSE(found == 12);
    TEST_ASSERT_FALSE(found == 16);
    TEST_ASSERT_FALSE(found == 14);
}

static void test_case_1(void)
{
    long found = sumOfDigits(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    long found = sumOfDigits(987654321L);
    (void)found;
    TEST_ASSERT_TRUE(found == 45);
    TEST_ASSERT_FALSE(found == 44);
    TEST_ASSERT_FALSE(found == 46);
    TEST_ASSERT_FALSE(found == 50);
}

static void test_case_3(void)
{
    long found = sumOfDigits(11111L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_4(void)
{
    long found = sumOfDigits(1001L);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 11);
}

static void test_case_5(void)
{
    long found = sumOfDigits(9999L);
    (void)found;
    TEST_ASSERT_TRUE(found == 36);
    TEST_ASSERT_FALSE(found == 35);
    TEST_ASSERT_FALSE(found == 37);
    TEST_ASSERT_FALSE(found == 34);
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
    return UNITY_END();
}
