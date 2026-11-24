/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_45.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long lst[] = {2L, 3L, 4L, 5L};
    long found = findProduct(4, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_1(void)
{
    static const long lst[] = {2L, 4L, 3L, 6L};
    long found = findProduct(4, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 24);
}

static void test_case_2(void)
{
    static const long lst[] = {1L, 2L, 5L, 4L};
    long found = findProduct(4, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 10);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    return UNITY_END();
}
