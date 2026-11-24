/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_49.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {2L, 4L, 6L, 8L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstOdd(4, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
}

static void test_case_1(void)
{
    static const long a[] = {3L, 4L, 6L, 8L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstOdd(4, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_2(void)
{
    static const long a[] = {2L, 4L, 5L, 8L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstOdd(4, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_3(void)
{
    static const long a[] = {7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstOdd(1, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_4(void)
{
    static const long a[] = {2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstOdd(1, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
}

static void test_case_5(void)
{
    static const long a[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstOdd(3, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
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
    RUN_TEST(test_case_5);
    return UNITY_END();
}
