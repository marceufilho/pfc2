/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_93.h"

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
    long found = SwapBitvectors(0L, 0L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 0 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
}

static void test_case_1(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapBitvectors(5L, 10L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 10 && out[1] == 5);
    TEST_ASSERT_FALSE(out[0] == 5 && out[1] == 10);
    TEST_ASSERT_FALSE(out[0] == 10 && out[1] == 10);
    TEST_ASSERT_FALSE(out[0] == 5 && out[1] == 5);
}

static void test_case_2(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapBitvectors(255L, 1L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 255);
    TEST_ASSERT_FALSE(out[0] == 255 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 254);
    TEST_ASSERT_FALSE(out[0] == 0 && out[1] == 255);
}

static void test_case_3(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapBitvectors(128L, 64L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 64 && out[1] == 128);
    TEST_ASSERT_FALSE(out[0] == 128 && out[1] == 64);
    TEST_ASSERT_FALSE(out[0] == 64 && out[1] == 64);
    TEST_ASSERT_FALSE(out[0] == 0 && out[1] == 128);
}

static void test_case_4(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapBitvectors(15L, 15L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 15 && out[1] == 15);
    TEST_ASSERT_FALSE(out[0] == 15 && out[1] == 16);
    TEST_ASSERT_FALSE(out[0] == 16 && out[1] == 15);
    TEST_ASSERT_FALSE(out[0] == 14 && out[1] == 15);
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
