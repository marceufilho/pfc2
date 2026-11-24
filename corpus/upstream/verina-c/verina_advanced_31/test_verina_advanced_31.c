/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_31.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {1L, 2L, 3L, 4L};
    long found = longestIncreasingSubseqLength(4, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_1(void)
{
    static const long xs[] = {4L, 3L, 2L, 1L};
    long found = longestIncreasingSubseqLength(4, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_2(void)
{
    static const long xs[] = {1L, 3L, 2L, 4L, 0L, 5L};
    long found = longestIncreasingSubseqLength(6, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_3(void)
{
    static const long xs[] = {0};
    long found = longestIncreasingSubseqLength(0, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long xs[] = {5L, 1L, 6L, 2L, 7L};
    long found = longestIncreasingSubseqLength(5, xs);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
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
