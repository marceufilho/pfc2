/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_43.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {-2L};
    long found = maxStrength(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == -2);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const long nums[] = {3L, -1L, -5L, 2L, 5L, -9L};
    long found = maxStrength(6, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1350);
    TEST_ASSERT_FALSE(found == 270);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_2(void)
{
    static const long nums[] = {-4L, -5L, -4L};
    long found = maxStrength(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 20);
    TEST_ASSERT_FALSE(found == 80);
    TEST_ASSERT_FALSE(found == -80);
    TEST_ASSERT_FALSE(found == -5);
}

static void test_case_3(void)
{
    static const long nums[] = {0L, -3L, 4L};
    long found = maxStrength(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -12);
}

static void test_case_4(void)
{
    static const long nums[] = {1L, -1L, -1L};
    long found = maxStrength(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
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
