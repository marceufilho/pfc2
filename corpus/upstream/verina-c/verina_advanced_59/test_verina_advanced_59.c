/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_59.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {0};
    long found = palindromeIgnoreNonAlnum(0, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const char s[] = {65, 32, 109, 97, 110, 44, 32, 97, 32, 112, 108, 97, 110, 44, 32, 97, 32, 99, 97, 110, 97, 108, 58, 32, 80, 97, 110, 97, 109, 97};
    long found = palindromeIgnoreNonAlnum(30, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const char s[] = {114, 97, 99, 101, 32, 97, 32, 99, 97, 114};
    long found = palindromeIgnoreNonAlnum(10, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    static const char s[] = {78, 111, 32, 39, 120, 39, 32, 105, 110, 32, 78, 105, 120, 111, 110};
    long found = palindromeIgnoreNonAlnum(15, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const char s[] = {97, 98, 99, 33, 33, 99, 98, 97, 63};
    long found = palindromeIgnoreNonAlnum(9, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_5(void)
{
    static const char s[] = {72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33};
    long found = palindromeIgnoreNonAlnum(13, s);
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
    RUN_TEST(test_case_5);
    return UNITY_END();
}
