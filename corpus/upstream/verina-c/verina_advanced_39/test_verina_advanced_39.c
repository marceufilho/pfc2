/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_39.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long lst[] = {1L, 2L, 3L};
    long found = maxOfList(3, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const long lst[] = {5L, 5L, 5L};
    long found = maxOfList(3, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const long lst[] = {10L, 1L, 9L};
    long found = maxOfList(3, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 9);
}

static void test_case_3(void)
{
    static const long lst[] = {7L};
    long found = maxOfList(1, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 6);
}

static void test_case_4(void)
{
    static const long lst[] = {0L, 0L, 0L, 0L};
    long found = maxOfList(4, lst);
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
    return UNITY_END();
}
