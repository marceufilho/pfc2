/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_16.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = insertionSort(0, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
}

static void test_case_1(void)
{
    static const long xs[] = {42L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = insertionSort(1, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 42);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 24);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 42 && out[1] == 42);
}

static void test_case_2(void)
{
    static const long xs[] = {3L, 1L, 4L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = insertionSort(4, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 3 && out[2] == 2 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 4 && out[1] == 3 && out[2] == 2 && out[3] == 1);
}

static void test_case_3(void)
{
    static const long xs[] = {5L, -1L, 0L, 10L, -1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = insertionSort(5, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == -1 && out[1] == -1 && out[2] == 0 && out[3] == 5 && out[4] == 10);
    TEST_ASSERT_FALSE(found == 5 && out[0] == -1 && out[1] == -1 && out[2] == 0 && out[3] == 10 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 10 && out[1] == 5 && out[2] == 0 && out[3] == -1 && out[4] == -1);
}

static void test_case_4(void)
{
    static const long xs[] = {2L, 2L, 2L, 2L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = insertionSort(5, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 2 && out[1] == 2 && out[2] == 2 && out[3] == 2 && out[4] == 2);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 2 && out[2] == 2 && out[3] == 2);
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
    return UNITY_END();
}
