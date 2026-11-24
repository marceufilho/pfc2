/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_42.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {49, 50, 51, 97, 98, 99, 52, 53, 54};
    long found = countDigits(9, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 6);
    TEST_ASSERT_FALSE(found == 5);
    TEST_ASSERT_FALSE(found == 7);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const char s[] = {110, 111, 32, 100, 105, 103, 105, 116, 115, 32, 104, 101, 114, 101, 33};
    long found = countDigits(15, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 3);
}

static void test_case_2(void)
{
    static const char s[] = {49, 50, 51, 52, 53, 54, 55, 56, 57, 48};
    long found = countDigits(10, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 10);
    TEST_ASSERT_FALSE(found == 9);
    TEST_ASSERT_FALSE(found == 11);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const char s[] = {0};
    long found = countDigits(0, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_4(void)
{
    static const char s[] = {97, 49, 98, 50, 99, 51};
    long found = countDigits(6, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 3);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 4);
    TEST_ASSERT_FALSE(found == 5);
}

static void test_case_5(void)
{
    static const char s[] = {48};
    long found = countDigits(1, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2);
    TEST_ASSERT_FALSE(found == 10);
}

static void test_case_6(void)
{
    static const char s[] = {97, 98, 99};
    long found = countDigits(3, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
    TEST_ASSERT_FALSE(found == 8);
    TEST_ASSERT_FALSE(found == 9);
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
