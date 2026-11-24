/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_8.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long gas[] = {1L, 2L, 3L, 4L, 5L};
    static const long cost[] = {3L, 4L, 5L, 1L, 2L};
    long found = canCompleteCircuit(5, gas, 5, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_1(void)
{
    static const long gas[] = {2L, 3L, 4L};
    static const long cost[] = {3L, 4L, 3L};
    long found = canCompleteCircuit(3, gas, 3, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const long gas[] = {5L, 1L, 2L, 3L, 4L};
    static const long cost[] = {4L, 4L, 1L, 5L, 1L};
    long found = canCompleteCircuit(5, gas, 5, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == 4);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_3(void)
{
    static const long gas[] = {3L, 3L, 4L};
    static const long cost[] = {3L, 4L, 4L};
    long found = canCompleteCircuit(3, gas, 3, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_4(void)
{
    static const long gas[] = {1L, 2L, 3L};
    static const long cost[] = {1L, 2L, 3L};
    long found = canCompleteCircuit(3, gas, 3, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_5(void)
{
    static const long gas[] = {1L, 2L, 3L, 4L};
    static const long cost[] = {2L, 2L, 2L, 2L};
    long found = canCompleteCircuit(4, gas, 4, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_6(void)
{
    static const long gas[] = {0L, 0L, 0L};
    static const long cost[] = {1L, 1L, 1L};
    long found = canCompleteCircuit(3, gas, 3, cost);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == -2);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
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
