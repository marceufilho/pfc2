/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_62.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long heights[] = {0L, 1L, 0L, 2L, 1L, 0L, 1L, 3L, 2L, 1L, 2L, 1L};
    long found = rain(12, heights);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_1(void)
{
    static const long heights[] = {4L, 2L, 0L, 3L, 2L, 5L};
    long found = rain(6, heights);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_2(void)
{
    static const long heights[] = {1L, 1L, 1L};
    long found = rain(3, heights);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    static const long heights[] = {10L, 5L};
    long found = rain(2, heights);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_4(void)
{
    static const long heights[] = {1L, 10L, 9L, 11L};
    long found = rain(4, heights);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_5(void)
{
    static const long heights[] = {0};
    long found = rain(0, heights);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 100);
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
    return UNITY_END();
}
