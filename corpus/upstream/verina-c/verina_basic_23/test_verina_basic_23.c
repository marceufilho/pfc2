/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_23.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {3L, 1L, 4L, 1L, 5L, 9L, 2L, 6L, 5L, 3L, 5L};
    long found = differenceMinMax(11, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 8);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_1(void)
{
    static const long a[] = {10L, 20L, 30L, 40L, 50L};
    long found = differenceMinMax(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 40);
    TEST_ASSERT_FALSE(found == 30);
    TEST_ASSERT_FALSE(found == 35);
    TEST_ASSERT_FALSE(found == 45);
}

static void test_case_2(void)
{
    static const long a[] = {-10L, -20L, -30L, -40L, -50L};
    long found = differenceMinMax(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 40);
    TEST_ASSERT_FALSE(found == 30);
    TEST_ASSERT_FALSE(found == 41);
    TEST_ASSERT_FALSE(found == 20);
}

static void test_case_3(void)
{
    static const long a[] = {7L};
    long found = differenceMinMax(1, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_4(void)
{
    static const long a[] = {5L, 5L, 5L, 5L};
    long found = differenceMinMax(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_5(void)
{
    static const long a[] = {1L, -1L, 2L, -2L};
    long found = differenceMinMax(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 0);
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
    return UNITY_END();
}
