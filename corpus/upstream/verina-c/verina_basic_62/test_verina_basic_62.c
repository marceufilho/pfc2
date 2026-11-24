/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_62.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L, 4L, 5L};
    long found = Find(5, a, 3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const long a[] = {5L, 7L, 5L, 9L};
    long found = Find(4, a, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_2(void)
{
    static const long a[] = {2L, 4L, 6L, 8L};
    long found = Find(4, a, 5L);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_3(void)
{
    static const long a[] = {0};
    long found = Find(0, a, 10L);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_4(void)
{
    static const long a[] = {0L, -3L, -1L, -3L};
    long found = Find(4, a, -3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
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
