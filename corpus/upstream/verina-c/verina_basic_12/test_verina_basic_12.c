/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_12.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = cubeSurfaceArea(3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 54);
    TEST_ASSERT_FALSE(found == 27);
    TEST_ASSERT_FALSE(found == 48);
    TEST_ASSERT_FALSE(found == 60);
}

static void test_case_1(void)
{
    long found = cubeSurfaceArea(1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    long found = cubeSurfaceArea(10L);
    (void)found;
    TEST_ASSERT_TRUE(found == 600);
    TEST_ASSERT_FALSE(found == 100);
    TEST_ASSERT_FALSE(found == 500);
    TEST_ASSERT_FALSE(found == 610);
}

static void test_case_3(void)
{
    long found = cubeSurfaceArea(5L);
    (void)found;
    TEST_ASSERT_TRUE(found == 150);
    TEST_ASSERT_FALSE(found == 25);
    TEST_ASSERT_FALSE(found == 100);
    TEST_ASSERT_FALSE(found == 125);
}

static void test_case_4(void)
{
    long found = cubeSurfaceArea(2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 24);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 16);
    TEST_ASSERT_FALSE(found == 20);
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
