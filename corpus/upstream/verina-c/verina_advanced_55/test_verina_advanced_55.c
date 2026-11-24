/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_55.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {1L, 2L, 2L, 3L};
    long found = mostFrequent(4, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    static const long xs[] = {4L, 4L, 5L, 5L, 4L};
    long found = mostFrequent(5, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_2(void)
{
    static const long xs[] = {9L};
    long found = mostFrequent(1, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long xs[] = {1L, 2L, 3L, 1L, 2L, 3L, 2L};
    long found = mostFrequent(7, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_4(void)
{
    static const long xs[] = {7L, 7L, 8L, 8L, 9L, 9L, 7L};
    long found = mostFrequent(7, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 9);
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
