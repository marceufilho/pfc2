/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_63.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {1L, 1L, 2L};
    long found = removeDuplicates(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_1(void)
{
    static const long nums[] = {0L, 0L, 1L, 1L, 1L, 2L, 2L, 3L, 3L, 4L};
    long found = removeDuplicates(10, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_2(void)
{
    static const long nums[] = {-1L, -1L, 0L, 1L, 2L, 2L, 3L};
    long found = removeDuplicates(7, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_3(void)
{
    static const long nums[] = {1L, 2L, 3L, 4L, 5L};
    long found = removeDuplicates(5, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_4(void)
{
    static const long nums[] = {1L, 1L, 1L, 1L};
    long found = removeDuplicates(4, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_5(void)
{
    static const long nums[] = {0};
    long found = removeDuplicates(0, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_6(void)
{
    static const long nums[] = {1L};
    long found = removeDuplicates(1, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_7(void)
{
    static const long nums[] = {-100L, -100L, -100L};
    long found = removeDuplicates(3, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_8(void)
{
    static const long nums[] = {-100L, -99L, -99L, -50L, 0L, 0L, 100L, 100L};
    long found = removeDuplicates(8, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 7);
}

static void test_case_9(void)
{
    static const long nums[] = {-1L, 0L, 0L, 0L, 1L, 2L, 2L, 3L, 4L, 4L, 5L};
    long found = removeDuplicates(11, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 7);
    TEST_ASSERT_FALSE(found == 6);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_10(void)
{
    static const long nums[] = {100L, 100L, 100L, 101L, 102L, 102L, 103L, 104L, 105L, 105L};
    long found = removeDuplicates(10, nums);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
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
    RUN_TEST(test_case_7);
    RUN_TEST(test_case_8);
    RUN_TEST(test_case_9);
    RUN_TEST(test_case_10);
    return UNITY_END();
}
