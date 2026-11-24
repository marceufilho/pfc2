/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_43.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = sumOfFourthPowerOfOddNumbers(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_1(void)
{
    long found = sumOfFourthPowerOfOddNumbers(1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    long found = sumOfFourthPowerOfOddNumbers(2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 82);
    TEST_ASSERT_FALSE(found == 81);
    TEST_ASSERT_FALSE(found == 83);
    TEST_ASSERT_FALSE(found == 80);
}

static void test_case_3(void)
{
    long found = sumOfFourthPowerOfOddNumbers(3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 707);
    TEST_ASSERT_FALSE(found == 706);
    TEST_ASSERT_FALSE(found == 708);
    TEST_ASSERT_FALSE(found == 700);
}

static void test_case_4(void)
{
    long found = sumOfFourthPowerOfOddNumbers(4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 3108);
    TEST_ASSERT_FALSE(found == 3107);
    TEST_ASSERT_FALSE(found == 3109);
    TEST_ASSERT_FALSE(found == 3000);
}

static void test_case_5(void)
{
    long found = sumOfFourthPowerOfOddNumbers(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 9669);
    TEST_ASSERT_FALSE(found == 9668);
    TEST_ASSERT_FALSE(found == 9670);
    TEST_ASSERT_FALSE(found == 9000);
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
