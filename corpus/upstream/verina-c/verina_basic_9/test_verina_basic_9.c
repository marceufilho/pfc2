/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_9.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L};
    static const long b[] = {4L, 5L, 6L};
    long found = hasCommonElement(3, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_1(void)
{
    static const long a[] = {1L, 2L, 3L};
    static const long b[] = {3L, 4L, 5L};
    long found = hasCommonElement(3, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const long a[] = {7L, 8L, 9L};
    static const long b[] = {10L, 11L, 7L};
    long found = hasCommonElement(3, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long a[] = {1L, 2L, 3L, 4L};
    static const long b[] = {5L, 6L, 7L, 8L};
    long found = hasCommonElement(4, a, 4, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long a[] = {1L, 2L, 3L, 4L};
    static const long b[] = {4L, 5L, 6L};
    long found = hasCommonElement(4, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_5(void)
{
    static const long a[] = {1L, 1L, 1L};
    static const long b[] = {1L, 2L, 1L};
    long found = hasCommonElement(3, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_6(void)
{
    static const long a[] = {0L};
    static const long b[] = {0L};
    long found = hasCommonElement(1, a, 1, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_7(void)
{
    static const long a[] = {0L};
    static const long b[] = {-1L, 1L};
    long found = hasCommonElement(1, a, 2, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
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
