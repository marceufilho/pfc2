/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_103.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {0L, 1L, 2L, 3L, 4L, 5L, 6L, 7L, 8L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = UpdateElements(9, a, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 9 && out[0] == 0 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 7 && out[5] == 5 && out[6] == 6 && out[7] == 516 && out[8] == 8);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 0 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 4 && out[5] == 5 && out[6] == 6 && out[7] == 516 && out[8] == 8);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 0 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 7 && out[5] == 5 && out[6] == 6 && out[7] == 7 && out[8] == 8);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 0 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 7 && out[5] == 5 && out[6] == 6 && out[7] == 516 && out[8] == 8 && out[9] == 0);
}

static void test_case_1(void)
{
    static const long a[] = {10L, 20L, 30L, 40L, 50L, 60L, 70L, 80L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = UpdateElements(8, a, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 53 && out[5] == 60 && out[6] == 70 && out[7] == 516);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 50 && out[5] == 60 && out[6] == 70 && out[7] == 80);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 53 && out[5] == 60 && out[6] == 70 && out[7] == 80);
}

static void test_case_2(void)
{
    static const long a[] = {-1L, -2L, -3L, -4L, -5L, -6L, -7L, -8L, -9L, -10L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = UpdateElements(10, a, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 10 && out[0] == -1 && out[1] == -2 && out[2] == -3 && out[3] == -4 && out[4] == -2 && out[5] == -6 && out[6] == -7 && out[7] == 516 && out[8] == -9 && out[9] == -10);
    TEST_ASSERT_FALSE(found == 10 && out[0] == -1 && out[1] == -2 && out[2] == -3 && out[3] == -4 && out[4] == -5 && out[5] == -6 && out[6] == -7 && out[7] == 516 && out[8] == -9 && out[9] == -10);
    TEST_ASSERT_FALSE(found == 10 && out[0] == -1 && out[1] == -2 && out[2] == -3 && out[3] == -4 && out[4] == -2 && out[5] == -6 && out[6] == -7 && out[7] == -8 && out[8] == -9 && out[9] == -10);
}

static void test_case_3(void)
{
    static const long a[] = {0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = UpdateElements(8, a, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 0 && out[4] == 3 && out[5] == 0 && out[6] == 0 && out[7] == 516);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 0 && out[4] == 0 && out[5] == 0 && out[6] == 0 && out[7] == 516);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 0 && out[4] == 3 && out[5] == 0 && out[6] == 0 && out[7] == 0);
}

static void test_case_4(void)
{
    static const long a[] = {5L, 5L, 5L, 5L, 5L, 5L, 5L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = UpdateElements(8, a, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 5 && out[1] == 5 && out[2] == 5 && out[3] == 5 && out[4] == 8 && out[5] == 5 && out[6] == 5 && out[7] == 516);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 5 && out[1] == 5 && out[2] == 5 && out[3] == 5 && out[4] == 5 && out[5] == 5 && out[6] == 5 && out[7] == 5);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 5 && out[1] == 5 && out[2] == 5 && out[3] == 5 && out[4] == 8 && out[5] == 5 && out[6] == 5 && out[7] == 5);
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
