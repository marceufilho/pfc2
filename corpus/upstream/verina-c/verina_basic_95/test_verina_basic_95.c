/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_95.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long arr[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = swap(5, arr, 1L, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 4 && out[2] == 3 && out[3] == 2 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 3 && out[2] == 2 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 4 && out[2] == 3 && out[3] == 2 && out[4] == 5 && out[5] == 0);
}

static void test_case_1(void)
{
    static const long arr[] = {10L, 20L, 30L, 40L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = swap(4, arr, 0L, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 40 && out[1] == 20 && out[2] == 30 && out[3] == 10);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 10 && out[1] == 40 && out[2] == 30 && out[3] == 20);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 10 && out[1] == 20 && out[2] == 40 && out[3] == 30);
}

static void test_case_2(void)
{
    static const long arr[] = {7L, 8L, 9L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = swap(3, arr, 1L, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 7 && out[1] == 9 && out[2] == 8);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 8 && out[1] == 7 && out[2] == 9);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 9 && out[1] == 8 && out[2] == 7);
}

static void test_case_3(void)
{
    static const long arr[] = {1L, 2L, 3L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = swap(4, arr, 0L, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 4 && out[3] == 3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 4 && out[1] == 2 && out[2] == 3 && out[3] == 1);
}

static void test_case_4(void)
{
    static const long arr[] = {-1L, -2L, -3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = swap(3, arr, 0L, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == -3 && out[1] == -2 && out[2] == -1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -1 && out[1] == -2 && out[2] == -3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -3 && out[1] == -1 && out[2] == -2);
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
