/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_20.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long arr[] = {2L, 3L, 2L, 4L};
    long found = uniqueProduct(4, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == 24);
    TEST_ASSERT_FALSE(found == 12);
    TEST_ASSERT_FALSE(found == 30);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const long arr[] = {5L, 5L, 5L, 5L};
    long found = uniqueProduct(4, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 25);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_2(void)
{
    static const long arr[] = {0};
    long found = uniqueProduct(0, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_3(void)
{
    static const long arr[] = {1L, 2L, 3L};
    long found = uniqueProduct(3, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_4(void)
{
    static const long arr[] = {0L, 2L, 3L};
    long found = uniqueProduct(3, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_5(void)
{
    static const long arr[] = {-1L, -2L, -1L, -3L};
    long found = uniqueProduct(4, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == -6);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == -3);
}

static void test_case_6(void)
{
    static const long arr[] = {10L, 10L, 20L, 20L, 30L};
    long found = uniqueProduct(5, arr);
    (void)found;
    TEST_ASSERT_TRUE(found == 6000);
    TEST_ASSERT_FALSE(found == 600);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 5000);
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
    RUN_TEST(test_case_6);
    return UNITY_END();
}
