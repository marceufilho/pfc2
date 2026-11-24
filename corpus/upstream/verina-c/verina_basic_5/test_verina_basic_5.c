/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_5.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = multiply(3L, 4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 12);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 11);
    TEST_ASSERT_FALSE(found == 15);
}

static void test_case_1(void)
{
    long found = multiply(3L, -4L);
    (void)found;
    TEST_ASSERT_TRUE(found == -12);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -11);
    TEST_ASSERT_FALSE(found == 12);
}

static void test_case_2(void)
{
    long found = multiply(-3L, 4L);
    (void)found;
    TEST_ASSERT_TRUE(found == -12);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -11);
    TEST_ASSERT_FALSE(found == 12);
}

static void test_case_3(void)
{
    long found = multiply(-3L, -4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 12);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 11);
    TEST_ASSERT_FALSE(found == -12);
}

static void test_case_4(void)
{
    long found = multiply(0L, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_5(void)
{
    long found = multiply(5L, 0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_6(void)
{
    long found = multiply(0L, 0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 5);
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
