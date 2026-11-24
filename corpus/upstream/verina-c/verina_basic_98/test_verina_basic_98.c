/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_98.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = Triple(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_1(void)
{
    long found = Triple(2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_2(void)
{
    long found = Triple(-4L);
    (void)found;
    TEST_ASSERT_TRUE(found == -12);
    TEST_ASSERT_FALSE(found == -8);
    TEST_ASSERT_FALSE(found == -10);
    TEST_ASSERT_FALSE(found == -16);
}

static void test_case_3(void)
{
    long found = Triple(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 30);
    TEST_ASSERT_FALSE(found == 20);
    TEST_ASSERT_FALSE(found == 25);
    TEST_ASSERT_FALSE(found == 35);
}

static void test_case_4(void)
{
    long found = Triple(-1L);
    (void)found;
    TEST_ASSERT_TRUE(found == -3);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -4);
    TEST_ASSERT_FALSE(found == 0);
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
