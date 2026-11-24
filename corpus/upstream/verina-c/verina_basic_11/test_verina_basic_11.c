/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_11.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = lastDigit(123L);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 23);
}

static void test_case_1(void)
{
    long found = lastDigit(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_2(void)
{
    long found = lastDigit(987654321L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_3(void)
{
    long found = lastDigit(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_4(void)
{
    long found = lastDigit(999L);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 99);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_5(void)
{
    long found = lastDigit(45L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 55);
}

static void test_case_6(void)
{
    long found = lastDigit(100L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_7(void)
{
    long found = lastDigit(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 6);
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
    return UNITY_END();
}
