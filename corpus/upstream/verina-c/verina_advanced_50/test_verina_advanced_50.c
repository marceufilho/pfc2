/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_50.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a1[] = {1L, 3L, 5L};
    static const long a2[] = {2L, 4L, 6L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(3, a1, 3, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 3 && out[2] == 5 && out[3] == 2 && out[4] == 4 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 2 && out[1] == 1 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6);
}

static void test_case_1(void)
{
    static const long a1[] = {0};
    static const long a2[] = {1L, 2L, 3L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(0, a1, 3, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 3 && out[1] == 2 && out[2] == 1);
}

static void test_case_2(void)
{
    static const long a1[] = {1L, 2L, 3L};
    static const long a2[] = {0};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(3, a1, 0, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 3 && out[1] == 2 && out[2] == 1);
}

static void test_case_3(void)
{
    static const long a1[] = {0};
    static const long a2[] = {0};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(0, a1, 0, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
}

static void test_case_4(void)
{
    static const long a1[] = {1L, 1L, 2L};
    static const long a2[] = {1L, 2L, 2L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(3, a1, 3, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 1 && out[2] == 1 && out[3] == 2 && out[4] == 2 && out[5] == 2);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 1 && out[2] == 2 && out[3] == 1 && out[4] == 2 && out[5] == 2);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 1 && out[1] == 2);
}

static void test_case_5(void)
{
    static const long a1[] = {10L, 20L, 30L};
    static const long a2[] = {5L, 15L, 25L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(3, a1, 3, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 5 && out[1] == 10 && out[2] == 15 && out[3] == 20 && out[4] == 25 && out[5] == 30);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 5 && out[4] == 15 && out[5] == 25);
}

static void test_case_6(void)
{
    static const long a1[] = {1L, 3L, 5L, 7L, 9L};
    static const long a2[] = {2L, 4L, 6L, 8L, 10L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(5, a1, 5, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 10 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5 && out[5] == 6 && out[6] == 7 && out[7] == 8 && out[8] == 9 && out[9] == 10);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 1 && out[1] == 3 && out[2] == 5 && out[3] == 7 && out[4] == 9 && out[5] == 2 && out[6] == 4 && out[7] == 6 && out[8] == 8 && out[9] == 10);
}

static void test_case_7(void)
{
    static const long a1[] = {5L, 5L, 5L};
    static const long a2[] = {5L, 5L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = mergeSorted(3, a1, 3, a2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 5 && out[1] == 5 && out[2] == 5 && out[3] == 5 && out[4] == 5 && out[5] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 5 && out[2] == 5);
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
