/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_14.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {104, 101, 108, 108, 111};
    long found = containsZ(5, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_1(void)
{
    static const char s[] = {122, 101, 98, 114, 97};
    long found = containsZ(5, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const char s[] = {90, 101, 98, 114, 97};
    long found = containsZ(5, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const char s[] = {0};
    long found = containsZ(0, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    static const char s[] = {99, 114, 97, 122, 121};
    long found = containsZ(5, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_5(void)
{
    static const char s[] = {65, 90};
    long found = containsZ(2, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_6(void)
{
    static const char s[] = {97, 98, 99};
    long found = containsZ(3, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_7(void)
{
    static const char s[] = {90, 122};
    long found = containsZ(2, s);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_8(void)
{
    static const char s[] = {110, 111, 32, 108, 101, 116, 116, 101, 114};
    long found = containsZ(9, s);
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
    RUN_TEST(test_case_6);
    RUN_TEST(test_case_7);
    RUN_TEST(test_case_8);
    return UNITY_END();
}
