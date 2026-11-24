/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_30.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {10L, 20L, 30L};
    static const long b[] = {3L, 7L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = elementWiseModulo(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 6 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 6 && out[2] == 0);
}

static void test_case_1(void)
{
    static const long a[] = {100L, 200L, 300L, 400L};
    static const long b[] = {10L, 20L, 30L, 50L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = elementWiseModulo(4, a, 4, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 0);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 1);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 0 && out[2] == 0 && out[3] == 0);
}

static void test_case_2(void)
{
    static const long a[] = {-10L, -20L, 30L};
    static const long b[] = {3L, -7L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = elementWiseModulo(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 2 && out[1] == 1 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -1 && out[1] == -5 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -1 && out[1] == -6 && out[2] == 1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == -6 && out[2] == 0);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    return UNITY_END();
}
