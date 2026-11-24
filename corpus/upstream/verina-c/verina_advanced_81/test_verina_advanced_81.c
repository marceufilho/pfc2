/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_81.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long arr[] = {1L, 1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = uniqueSorted(4, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 1 && out[2] == 2 && out[3] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 3 && out[2] == 1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 3 && out[2] == 2);
}

static void test_case_1(void)
{
    static const long arr[] = {3L, 3L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = uniqueSorted(3, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 3 && out[1] == 3 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 3 && out[1] == 3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 3 && out[1] == 3 && out[2] == 3 && out[3] == 3);
}

static void test_case_2(void)
{
    static const long arr[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = uniqueSorted(0, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 999);
}

static void test_case_3(void)
{
    static const long arr[] = {5L, 2L, 2L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = uniqueSorted(4, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 2 && out[1] == 5);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 5 && out[1] == 2);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 2 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 2);
}

static void test_case_4(void)
{
    static const long arr[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = uniqueSorted(5, arr, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 3 && out[2] == 4 && out[3] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 4 && out[2] == 3 && out[3] == 2 && out[4] == 1);
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
