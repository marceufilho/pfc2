/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_47.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L, 4L, 5L};
    long found = arraySum(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 15);
    TEST_ASSERT_FALSE(found == 14);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 16);
}

static void test_case_1(void)
{
    static const long a[] = {13L, 14L, 15L, 16L, 17L};
    long found = arraySum(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 75);
    TEST_ASSERT_FALSE(found == 74);
    TEST_ASSERT_FALSE(found == 76);
    TEST_ASSERT_FALSE(found == 70);
}

static void test_case_2(void)
{
    static const long a[] = {-1L, -2L, -3L};
    long found = arraySum(3, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -6);
    TEST_ASSERT_FALSE(found == -5);
    TEST_ASSERT_FALSE(found == -7);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long a[] = {10L, -10L};
    long found = arraySum(2, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == -5);
    TEST_ASSERT_FALSE(found == 10);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    RUN_TEST(test_case_3);
    return UNITY_END();
}
