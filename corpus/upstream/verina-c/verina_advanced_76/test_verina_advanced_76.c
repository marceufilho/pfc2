/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_76.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {1L, 1L, 1L, 2L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = topKFrequent(6, nums, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 1 && out[1] == 3);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 2 && out[1] == 3);
}

static void test_case_1(void)
{
    static const long nums[] = {4L, 1L, -1L, 2L, -1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = topKFrequent(7, nums, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == -1 && out[1] == 2);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -1 && out[1] == 4);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 4 && out[1] == 3);
}

static void test_case_2(void)
{
    static const long nums[] = {5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = topKFrequent(1, nums, 1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 5);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_3(void)
{
    static const long nums[] = {7L, 7L, 7L, 8L, 8L, 9L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = topKFrequent(6, nums, 1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 7);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 8);
}

static void test_case_4(void)
{
    static const long nums[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = topKFrequent(0, nums, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
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
