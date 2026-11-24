/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_7.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long digits[] = {1L, 0L, 1L};
    long found = binaryToDecimal(3, digits);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_1(void)
{
    static const long digits[] = {1L, 1L, 1L, 1L};
    long found = binaryToDecimal(4, digits);
    (void)found;
    TEST_ASSERT_TRUE(found == 15);
    TEST_ASSERT_FALSE(found == 14);
    TEST_ASSERT_FALSE(found == 16);
}

static void test_case_2(void)
{
    static const long digits[] = {0L, 0L, 0L};
    long found = binaryToDecimal(3, digits);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_3(void)
{
    static const long digits[] = {1L, 0L, 0L, 0L, 0L};
    long found = binaryToDecimal(5, digits);
    (void)found;
    TEST_ASSERT_TRUE(found == 16);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const long digits[] = {0};
    long found = binaryToDecimal(0, digits);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_5(void)
{
    static const long digits[] = {1L};
    long found = binaryToDecimal(1, digits);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
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
    return UNITY_END();
}
