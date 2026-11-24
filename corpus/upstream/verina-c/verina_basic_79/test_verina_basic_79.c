/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_79.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {3L, 7L, 5L, 2L, 9L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(5, a, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 7 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 7 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 5 && out[1] == 4);
}

static void test_case_1(void)
{
    static const long a[] = {10L, 10L, 5L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(4, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 10 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 10 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 7 && out[1] == 3);
}

static void test_case_2(void)
{
    static const long a[] = {1L, 3L, 3L, 3L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(5, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 3 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 2 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 3 && out[1] == 3);
}

static void test_case_3(void)
{
    static const long a[] = {5L, 4L, 4L, 6L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(5, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 5 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 4 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 5 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 6 && out[1] == 3);
}

static void test_case_4(void)
{
    static const long a[] = {2L, 8L, 7L, 7L, 7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(5, a, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 8 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 7 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 8 && out[1] == 3);
}

static void test_case_5(void)
{
    static const long a[] = {100L, 50L, 1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(5, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 100 && out[1] == 4);
    TEST_ASSERT_FALSE(out[0] == 100 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 50 && out[1] == 4);
}

static void test_case_6(void)
{
    static const long a[] = {1L, 10L, 5L, 15L, 20L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = onlineMax(5, a, 1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 4);
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
    return UNITY_END();
}
