/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_19.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {65, 32, 109, 97, 110, 44, 32, 97, 32, 112, 108, 97, 110, 44, 32, 97, 32, 99, 97, 110, 97, 108, 44, 32, 80, 97, 110, 97, 109, 97};
    long found = isCleanPalindrome(30, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const char s[] = {78, 111, 32, 108, 101, 109, 111, 110, 44, 32, 110, 111, 32, 109, 101, 108, 111, 110};
    long found = isCleanPalindrome(18, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const char s[] = {79, 112, 101, 110, 65, 73};
    long found = isCleanPalindrome(6, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    static const char s[] = {87, 97, 115, 32, 105, 116, 32, 97, 32, 99, 97, 114, 32, 111, 114, 32, 97, 32, 99, 97, 116, 32, 73, 32, 115, 97, 119, 63};
    long found = isCleanPalindrome(28, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const char s[] = {72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33};
    long found = isCleanPalindrome(13, s);
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
