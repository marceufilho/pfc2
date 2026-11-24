/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_92.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapArithmetic(3L, 4L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 4 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 3 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 3 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 4 && out[1] == 4);
}

static void test_case_1(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapArithmetic(-1L, 10L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 10 && out[1] == -1);
    TEST_ASSERT_FALSE(out[0] == -1 && out[1] == 10);
    TEST_ASSERT_FALSE(out[0] == 10 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == -10 && out[1] == -1);
}

static void test_case_2(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapArithmetic(0L, 0L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 0 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == -1 && out[1] == 0);
}

static void test_case_3(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapArithmetic(100L, 50L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 50 && out[1] == 100);
    TEST_ASSERT_FALSE(out[0] == 100 && out[1] == 50);
    TEST_ASSERT_FALSE(out[0] == 50 && out[1] == 50);
    TEST_ASSERT_FALSE(out[0] == 100 && out[1] == 100);
}

static void test_case_4(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapArithmetic(-5L, -10L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == -10 && out[1] == -5);
    TEST_ASSERT_FALSE(out[0] == -5 && out[1] == -10);
    TEST_ASSERT_FALSE(out[0] == -10 && out[1] == -10);
    TEST_ASSERT_FALSE(out[0] == -5 && out[1] == -5);
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
