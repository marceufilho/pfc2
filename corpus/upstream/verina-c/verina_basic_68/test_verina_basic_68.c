/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_68.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 3L, 5L, 7L, 9L};
    long found = LinearSearch(5, a, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_1(void)
{
    static const long a[] = {2L, 4L, 6L, 8L};
    long found = LinearSearch(4, a, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    static const long a[] = {5L, 5L, 5L};
    long found = LinearSearch(3, a, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_3(void)
{
    static const long a[] = {10L, 9L, 8L, 7L};
    long found = LinearSearch(4, a, 10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_4(void)
{
    static const long a[] = {1L, 2L, 3L, 3L, 4L};
    long found = LinearSearch(5, a, 3L);
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
