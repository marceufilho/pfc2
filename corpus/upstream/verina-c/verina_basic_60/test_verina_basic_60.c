/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_60.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long arr[] = {1L, 2L, 3L, 4L, 5L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(6, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 2 && out[1] == 4 && out[2] == 6);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 4 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 3 && out[2] == 6);
}

static void test_case_1(void)
{
    static const long arr[] = {0L, -2L, 3L, -4L, 7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(5, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == -2 && out[2] == -4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 3 && out[2] == -4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == -2 && out[2] == 3);
}

static void test_case_2(void)
{
    static const long arr[] = {1L, 3L, 5L, 7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(4, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 1);
}

static void test_case_3(void)
{
    static const long arr[] = {2L, 4L, 8L, 10L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(4, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 2 && out[1] == 4 && out[2] == 8 && out[3] == 10);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 4 && out[2] == 8 && out[3] == 9);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 2 && out[1] == 4 && out[2] == 8 && out[3] == 10 && out[4] == 12);
}

static void test_case_4(void)
{
    static const long arr[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(0, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 1 && out[1] == 2);
}

static void test_case_5(void)
{
    static const long arr[] = {2L, 4L, 2L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(4, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 2 && out[1] == 4 && out[2] == 2 && out[3] == 6);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 2 && out[2] == 4 && out[3] == 6);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 4 && out[1] == 2 && out[2] == 6);
}

static void test_case_6(void)
{
    static const long arr[] = {1L, 2L, 8L, 2L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = FindEvenNumbers(5, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 2 && out[1] == 8 && out[2] == 2);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 2 && out[2] == 8);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 8 && out[1] == 2 && out[2] == 2);
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
