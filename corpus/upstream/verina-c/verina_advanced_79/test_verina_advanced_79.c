/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_79.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {2L, 7L, 11L, 15L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = twoSum(4, nums, 9L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0 && out[2] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1 && out[2] == 2);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_1(void)
{
    static const long nums[] = {3L, 2L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = twoSum(3, nums, 6L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 1 && out[2] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0 && out[2] == 2);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_2(void)
{
    static const long nums[] = {3L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = twoSum(2, nums, 6L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0 && out[2] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1 && out[2] == 1);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_3(void)
{
    static const long nums[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = twoSum(3, nums, 7L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0 && out[2] == 2);
}

static void test_case_4(void)
{
    static const long nums[] = {0L, 4L, 3L, 0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = twoSum(4, nums, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0 && out[2] == 3);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1 && out[2] == 2);
    TEST_ASSERT_FALSE(out[0] == 0);
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
