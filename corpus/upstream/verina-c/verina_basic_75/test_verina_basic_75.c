/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_75.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {5L, 3L, 8L, 2L, 7L};
    long found = minArray(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_1(void)
{
    static const long a[] = {10L, 10L, 10L};
    long found = minArray(3, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 11);
}

static void test_case_2(void)
{
    static const long a[] = {-1L, -5L, 3L, 0L};
    long found = minArray(4, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -5);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_3(void)
{
    static const long a[] = {42L};
    long found = minArray(1, a);
    (void)found;
    TEST_ASSERT_TRUE(found == 42);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -42);
    TEST_ASSERT_FALSE(found == 100);
}

static void test_case_4(void)
{
    static const long a[] = {3L, -2L, 0L, -2L, 5L};
    long found = minArray(5, a);
    (void)found;
    TEST_ASSERT_TRUE(found == -2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 3);
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
    return UNITY_END();
}
