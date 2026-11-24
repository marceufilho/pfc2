/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_49.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long arr1[] = {1L, 3L, 5L};
    static const long arr2[] = {2L, 4L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSortedLists(3, arr1, 3, arr2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 3 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 4 && out[2] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 3 && out[2] == 2 && out[3] == 4 && out[4] == 5 && out[5] == 6);
}

static void test_case_1(void)
{
    static const long arr1[] = {0};
    static const long arr2[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSortedLists(0, arr1, 0, arr2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 999);
}

static void test_case_2(void)
{
    static const long arr1[] = {-2L, 0L, 1L};
    static const long arr2[] = {-3L, -1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSortedLists(3, arr1, 2, arr2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == -3 && out[1] == -2 && out[2] == -1 && out[3] == 0 && out[4] == 1);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -3 && out[1] == -1);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -2 && out[1] == 0 && out[2] == 1);
}

static void test_case_3(void)
{
    static const long arr1[] = {10L, 20L, 30L};
    static const long arr2[] = {5L, 25L, 35L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSortedLists(3, arr1, 3, arr2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 5 && out[1] == 10 && out[2] == 20 && out[3] == 25 && out[4] == 30 && out[5] == 35);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 20 && out[2] == 30);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 25 && out[2] == 35);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 10 && out[1] == 20 && out[2] == 25 && out[3] == 30 && out[4] == 35);
}

static void test_case_4(void)
{
    static const long arr1[] = {1L, 2L, 2L};
    static const long arr2[] = {2L, 3L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSortedLists(3, arr1, 3, arr2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 2 && out[3] == 2 && out[4] == 3 && out[5] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 2 && out[1] == 2 && out[2] == 2 && out[3] == 3 && out[4] == 3);
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
