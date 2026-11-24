/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_77.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long height[] = {0L, 1L, 0L, 2L, 1L, 0L, 1L, 3L, 2L, 1L, 2L, 1L};
    long found = trapRainWater(12, height);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_1(void)
{
    static const long height[] = {4L, 2L, 0L, 3L, 2L, 5L};
    long found = trapRainWater(6, height);
    (void)found;
    TEST_ASSERT_TRUE(found == 9);
    TEST_ASSERT_FALSE(found == 8);
}

static void test_case_2(void)
{
    static const long height[] = {1L, 0L, 2L};
    long found = trapRainWater(3, height);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_3(void)
{
    static const long height[] = {3L, 0L, 1L, 3L, 0L, 5L};
    long found = trapRainWater(6, height);
    (void)found;
    TEST_ASSERT_TRUE(found == 8);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_4(void)
{
    static const long height[] = {0L, 1L, 2L, 3L, 4L, 5L};
    long found = trapRainWater(6, height);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_5(void)
{
    static const long height[] = {0};
    long found = trapRainWater(0, height);
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
    return UNITY_END();
}
