/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_11.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long lst[] = {1L, 2L, 1L, 1L};
    long found = findMajorityElement(4, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_1(void)
{
    static const long lst[] = {1L, 2L, 3L, 4L};
    long found = findMajorityElement(4, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == 4);
}

static void test_case_2(void)
{
    static const long lst[] = {2L, 2L, 2L, 2L, 3L, 3L};
    long found = findMajorityElement(6, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_3(void)
{
    static const long lst[] = {0};
    long found = findMajorityElement(0, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const long lst[] = {5L, 5L, 5L, 5L, 5L, 5L};
    long found = findMajorityElement(6, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == 5);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == -1);
}

static void test_case_5(void)
{
    static const long lst[] = {-1L, -1L, -1L, 2L, 2L};
    long found = findMajorityElement(5, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == -1);
    TEST_ASSERT_FALSE(found == 2);
}

static void test_case_6(void)
{
    static const long lst[] = {-3L, -3L, -3L, -3L, 1L};
    long found = findMajorityElement(5, lst);
    (void)found;
    TEST_ASSERT_TRUE(found == -3);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == -1);
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
