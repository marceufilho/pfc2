/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_51.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 3L, 5L};
    static const long b[] = {2L, 4L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSorted(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 3 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 4 && out[2] == 6);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 6 && out[1] == 5 && out[2] == 4);
}

static void test_case_1(void)
{
    static const long a[] = {1L, 2L};
    static const long b[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSorted(2, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 1 && out[2] == 2 && out[3] == 2 && out[4] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
}

static void test_case_2(void)
{
    static const long a[] = {0};
    static const long b[] = {4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSorted(0, a, 2, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 4 && out[1] == 5);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long a[] = {0L, 3L, 4L};
    static const long b[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSorted(3, a, 0, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == 3 && out[2] == 4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 4 && out[1] == 3 && out[2] == 0);
}

static void test_case_4(void)
{
    static const long a[] = {1L, 4L, 6L};
    static const long b[] = {2L, 3L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = mergeSorted(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 4 && out[2] == 6 && out[3] == 2 && out[4] == 3 && out[5] == 5);
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
