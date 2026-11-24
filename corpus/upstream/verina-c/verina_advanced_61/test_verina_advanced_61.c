/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_61.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums[] = {1L, 2L, 3L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = productExceptSelf(4, nums, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 24 && out[1] == 12 && out[2] == 8 && out[3] == 6);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 24 && out[1] == 12 && out[2] == 8 && out[3] == 0);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
}

static void test_case_1(void)
{
    static const long nums[] = {-1L, 1L, 0L, -3L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = productExceptSelf(5, nums, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 0 && out[1] == 0 && out[2] == 9 && out[3] == 0 && out[4] == 0);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 0 && out[4] == 0);
}

static void test_case_2(void)
{
    static const long nums[] = {2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = productExceptSelf(2, nums, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 3 && out[1] == 2);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 6);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 6 && out[1] == 6);
}

static void test_case_3(void)
{
    static const long nums[] = {5L, 5L, 5L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = productExceptSelf(4, nums, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 125 && out[1] == 125 && out[2] == 125 && out[3] == 125);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 5);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 25 && out[1] == 25 && out[2] == 25 && out[3] == 25);
}

static void test_case_4(void)
{
    static const long nums[] = {0L, 1L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = productExceptSelf(3, nums, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 2 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 1 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 2 && out[1] == 0);
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
