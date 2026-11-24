/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_74.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L, 4L, 5L};
    long found = maxArray(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    static const long a[] = {5L, 3L, 4L, 1L, 2L};
    long found = maxArray(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_2(void)
{
    static const long a[] = {7L};
    long found = maxArray(1, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_3(void)
{
    static const long a[] = {-1L, -5L, -3L, -4L};
    long found = maxArray(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -3);
    TEST_ASSERT_FALSE(found == -4);
}

static void test_case_4(void)
{
    static const long a[] = {-10L, -20L, -30L, -5L, -15L};
    long found = maxArray(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -5);
    TEST_ASSERT_FALSE(found == -10);
    TEST_ASSERT_FALSE(found == -15);
    TEST_ASSERT_FALSE(found == -20);
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
