/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_54.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 3L, 5L};
    static const long b[] = {2L, 4L, 6L};
    long found = CanyonSearch(3, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    static const long a[] = {-5L, -2L, 0L};
    static const long b[] = {1L, 3L};
    long found = CanyonSearch(3, a, 2, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    static const long a[] = {10L, 20L, 30L};
    static const long b[] = {5L, 15L, 25L};
    long found = CanyonSearch(3, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_3(void)
{
    static const long a[] = {1L, 2L, 3L, 4L, 5L};
    static const long b[] = {3L};
    long found = CanyonSearch(5, a, 1, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_4(void)
{
    static const long a[] = {-10L, -5L, 0L, 5L, 10L};
    static const long b[] = {-3L, 2L, 8L};
    long found = CanyonSearch(5, a, 3, b);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
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
