/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_106.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L};
    static const long b[] = {4L, 5L, 6L};
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = arraySum(3, a, 3, b, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 5 && out[1] == 7 && out[2] == 9);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 6 && out[2] == 9);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 4 && out[1] == 7 && out[2] == 9);
}

static void test_case_1(void)
{
    static const long a[] = {0L, 0L, 0L};
    static const long b[] = {0L, 0L, 0L};
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = arraySum(3, a, 3, b, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == 0);
}

static void test_case_2(void)
{
    static const long a[] = {-1L, 2L, 3L};
    static const long b[] = {1L, -2L, 4L};
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = arraySum(3, a, 3, b, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 7);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 1 && out[2] == 7);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 6);
}

static void test_case_3(void)
{
    static const long a[] = {10L};
    static const long b[] = {-10L};
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = arraySum(1, a, 1, b, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == -1);
}

static void test_case_4(void)
{
    static const long a[] = {100L, 200L, 300L};
    static const long b[] = {100L, 200L, 300L};
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = arraySum(3, a, 3, b, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 200 && out[1] == 400 && out[2] == 600);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 200 && out[1] == 400 && out[2] == 601);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 199 && out[1] == 400 && out[2] == 600);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 200 && out[1] == 399 && out[2] == 600);
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
