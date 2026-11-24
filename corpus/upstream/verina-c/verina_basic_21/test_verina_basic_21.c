/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_21.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long sub[] = {1L, 2L};
    static const long main[] = {3L, 1L, 2L, 4L};
    long found = isSublist(2, sub, 4, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const long sub[] = {2L, 3L};
    static const long main[] = {3L, 1L, 2L, 4L};
    long found = isSublist(2, sub, 4, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_2(void)
{
    static const long sub[] = {3L, 1L};
    static const long main[] = {3L, 1L, 2L, 4L};
    long found = isSublist(2, sub, 4, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long sub[] = {4L};
    static const long main[] = {3L, 1L, 2L, 4L};
    long found = isSublist(1, sub, 4, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const long sub[] = {5L};
    static const long main[] = {3L, 1L, 2L, 4L};
    long found = isSublist(1, sub, 4, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_5(void)
{
    static const long sub[] = {0};
    static const long main[] = {3L, 1L, 2L, 4L};
    long found = isSublist(0, sub, 4, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_6(void)
{
    static const long sub[] = {1L, 2L};
    static const long main[] = {0};
    long found = isSublist(2, sub, 0, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_7(void)
{
    static const long sub[] = {0};
    static const long main[] = {0};
    long found = isSublist(0, sub, 0, main);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
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
    return UNITY_END();
}
