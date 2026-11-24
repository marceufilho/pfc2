/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_40.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long s[] = {5L, 3L, 1L, 4L, 2L};
    long found = secondSmallest(5, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_1(void)
{
    static const long s[] = {7L, 2L, 5L, 3L};
    long found = secondSmallest(4, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_2(void)
{
    static const long s[] = {10L, 20L};
    long found = secondSmallest(2, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 20);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 30);
    TEST_ASSERT_FALSE(found == 25);
}

static void test_case_3(void)
{
    static const long s[] = {20L, 10L};
    long found = secondSmallest(2, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 20);
    TEST_ASSERT_FALSE(found == 10);
    TEST_ASSERT_FALSE(found == 30);
    TEST_ASSERT_FALSE(found == 15);
}

static void test_case_4(void)
{
    static const long s[] = {3L, 1L, 2L};
    long found = secondSmallest(3, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_5(void)
{
    static const long s[] = {1L, 1L, 2L};
    long found = secondSmallest(3, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 0);
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
    RUN_TEST(test_case_5);
    return UNITY_END();
}
