/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_86.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotate(5, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 3 && out[1] == 4 && out[2] == 5 && out[3] == 1 && out[4] == 2);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 2 && out[1] == 3 && out[2] == 4 && out[3] == 5 && out[4] == 1);
}

static void test_case_1(void)
{
    static const long a[] = {10L, 20L, 30L, 40L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotate(4, a, 1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 20 && out[1] == 30 && out[2] == 40 && out[3] == 10);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 40 && out[1] == 10 && out[2] == 20 && out[3] == 30);
}

static void test_case_2(void)
{
    static const long a[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotate(0, a, 5L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
}

static void test_case_3(void)
{
    static const long a[] = {7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotate(1, a, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 7);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 8);
}

static void test_case_4(void)
{
    static const long a[] = {-1L, -2L, -3L, -4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotate(4, a, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == -4 && out[1] == -1 && out[2] == -2 && out[3] == -3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == -1 && out[1] == -2 && out[2] == -3 && out[3] == -4);
    TEST_ASSERT_FALSE(found == 4 && out[0] == -3 && out[1] == -4 && out[2] == -1 && out[3] == -2);
}

static void test_case_5(void)
{
    static const long a[] = {5L, 10L, 15L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotate(3, a, 5L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 15 && out[1] == 5 && out[2] == 10);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 10 && out[2] == 15);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 15 && out[2] == 5);
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
