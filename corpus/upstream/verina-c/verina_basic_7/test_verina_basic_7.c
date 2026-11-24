/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_7.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_1(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 11);
    TEST_ASSERT_FALSE(found == 12);
}

static void test_case_3(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 35);
    TEST_ASSERT_FALSE(found == 30);
    TEST_ASSERT_FALSE(found == 34);
    TEST_ASSERT_FALSE(found == 36);
}

static void test_case_4(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 84);
    TEST_ASSERT_FALSE(found == 80);
    TEST_ASSERT_FALSE(found == 85);
    TEST_ASSERT_FALSE(found == 90);
}

static void test_case_5(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 165);
    TEST_ASSERT_FALSE(found == 160);
    TEST_ASSERT_FALSE(found == 166);
    TEST_ASSERT_FALSE(found == 170);
}

static void test_case_6(void)
{
    long found = sumOfSquaresOfFirstNOddNumbers(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1330);
    TEST_ASSERT_FALSE(found == 1320);
    TEST_ASSERT_FALSE(found == 1331);
    TEST_ASSERT_FALSE(found == 1340);
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
    return UNITY_END();
}
