/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_48.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long list[] = {5L, 2L, 9L, 1L, 5L, 6L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(6, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 5 && out[3] == 5 && out[4] == 6 && out[5] == 9);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 5 && out[1] == 2 && out[2] == 9 && out[3] == 1 && out[4] == 5 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 9 && out[1] == 6 && out[2] == 5 && out[3] == 5 && out[4] == 2 && out[5] == 1);
}

static void test_case_1(void)
{
    static const long list[] = {3L, 1L, 4L, 1L, 5L, 9L, 2L, 6L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(8, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 1 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 4 && out[5] == 5 && out[6] == 6 && out[7] == 9);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 3 && out[1] == 1 && out[2] == 4 && out[3] == 1 && out[4] == 5 && out[5] == 9 && out[6] == 2 && out[7] == 6);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 9 && out[1] == 6 && out[2] == 5 && out[3] == 4 && out[4] == 3 && out[5] == 2 && out[6] == 1 && out[7] == 1);
}

static void test_case_2(void)
{
    static const long list[] = {0};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(0, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
}

static void test_case_3(void)
{
    static const long list[] = {1L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(1, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const long list[] = {5L, 5L, 5L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(4, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 5 && out[1] == 5 && out[2] == 5 && out[3] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 5 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 5 && out[2] == 5 && out[3] == 5 && out[4] == 5);
}

static void test_case_5(void)
{
    static const long list[] = {9L, 8L, 7L, 6L, 5L, 4L, 3L, 2L, 1L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(9, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 9 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6 && out[6] == 7 && out[7] == 8 && out[8] == 9);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 9 && out[1] == 8 && out[2] == 7 && out[3] == 6 && out[4] == 5 && out[5] == 4 && out[6] == 3 && out[7] == 2 && out[8] == 1);
}

static void test_case_6(void)
{
    static const long list[] = {1L, 2L, 3L, 4L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(5, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 4 && out[2] == 3 && out[3] == 2 && out[4] == 1);
}

static void test_case_7(void)
{
    static const long list[] = {-3L, -1L, -5L, -2L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSort(4, list, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == -5 && out[1] == -3 && out[2] == -2 && out[3] == -1);
    TEST_ASSERT_FALSE(found == 4 && out[0] == -3 && out[1] == -1 && out[2] == -5 && out[3] == -2);
    TEST_ASSERT_FALSE(found == 4 && out[0] == -1 && out[1] == -2 && out[2] == -3 && out[3] == -5);
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
