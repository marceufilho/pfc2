/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_96.h"

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
    long found = SwapSimultaneous(3L, 4L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 4 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 3 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 3 && out[1] == 3);
}

static void test_case_1(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapSimultaneous(-10L, 20L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 20 && out[1] == -10);
    TEST_ASSERT_FALSE(out[0] == 20 && out[1] == -20);
    TEST_ASSERT_FALSE(out[0] == -10 && out[1] == 20);
}

static void test_case_2(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapSimultaneous(0L, 0L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 0 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
}

static void test_case_3(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapSimultaneous(123L, -456L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == -456 && out[1] == 123);
    TEST_ASSERT_FALSE(out[0] == 123 && out[1] == -456);
    TEST_ASSERT_FALSE(out[0] == -123 && out[1] == 456);
}

static void test_case_4(void)
{
    long out[8];
    for (int i = 0; i < 8; i++) { out[i] = 77; }
    long found = SwapSimultaneous(-1L, -2L, 8, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == -2 && out[1] == -1);
    TEST_ASSERT_FALSE(out[0] == -1 && out[1] == -2);
    TEST_ASSERT_FALSE(out[0] == -2 && out[1] == 2);
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
