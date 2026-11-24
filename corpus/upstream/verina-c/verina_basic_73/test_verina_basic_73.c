/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_73.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {97, 98, 99};
    static const char p[] = {97, 63, 99};
    long found = Match(3, s, 3, p);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const char s[] = {104, 101, 108, 108, 111};
    static const char p[] = {104, 101, 63, 108, 111};
    long found = Match(5, s, 5, p);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const char s[] = {119, 111, 114, 108, 100};
    static const char p[] = {119, 63, 114, 108, 100};
    long found = Match(5, s, 5, p);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const char s[] = {116, 101, 115, 116};
    static const char p[] = {116, 101, 63, 116};
    long found = Match(4, s, 4, p);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const char s[] = {97, 98, 99};
    static const char p[] = {97, 98, 100};
    long found = Match(3, s, 3, p);
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
