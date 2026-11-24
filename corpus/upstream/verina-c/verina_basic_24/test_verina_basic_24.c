/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_24.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {2L, 3L, 4L, 5L};
    long found = firstEvenOddDifference(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -3);
}

static void test_case_1(void)
{
    static const long a[] = {1L, 4L, 6L, 8L};
    long found = firstEvenOddDifference(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    static const long a[] = {7L, 2L, 9L, 4L};
    long found = firstEvenOddDifference(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -5);
    TEST_ASSERT_FALSE(found == -3);
    TEST_ASSERT_FALSE(found == -6);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_3(void)
{
    static const long a[] = {2L, 2L, 3L, 3L};
    long found = firstEvenOddDifference(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -2);
}

static void test_case_4(void)
{
    static const long a[] = {1L, 1L, 2L, 2L};
    long found = firstEvenOddDifference(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == -1);
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
