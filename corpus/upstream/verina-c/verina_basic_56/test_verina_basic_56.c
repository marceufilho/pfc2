/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_56.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long src[] = {10L, 20L, 30L, 40L, 50L};
    static const long dest[] = {1L, 2L, 3L, 4L, 5L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = copy(5, src, 1L, 6, dest, 3L, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 20 && out[4] == 30 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 10 && out[4] == 30 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 20 && out[4] == 40 && out[5] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 20 && out[3] == 30 && out[4] == 6 && out[5] == 0);
}

static void test_case_1(void)
{
    static const long src[] = {5L, 6L, 7L, 8L};
    static const long dest[] = {9L, 9L, 9L, 9L, 9L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = copy(4, src, 0L, 5, dest, 1L, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 9 && out[1] == 5 && out[2] == 6 && out[3] == 7 && out[4] == 9);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 9 && out[1] == 9 && out[2] == 5 && out[3] == 7 && out[4] == 9);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 9 && out[1] == 5 && out[2] == 7 && out[3] == 6 && out[4] == 9);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 9 && out[1] == 5 && out[2] == 6 && out[3] == 9 && out[4] == 9);
}

static void test_case_2(void)
{
    static const long src[] = {100L, 200L};
    static const long dest[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = copy(2, src, 0L, 3, dest, 1L, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 0);
}

static void test_case_3(void)
{
    static const long src[] = {10L, 20L, 30L, 40L, 50L};
    static const long dest[] = {0L, 0L, 0L, 0L, 0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = copy(5, src, 0L, 5, dest, 0L, 5L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 50);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 60);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 0 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 50);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40 && out[4] == 0);
}

static void test_case_4(void)
{
    static const long src[] = {7L, 8L, 9L, 10L};
    static const long dest[] = {1L, 2L, 3L, 4L, 5L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = copy(4, src, 2L, 6, dest, 4L, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 9 && out[5] == 10);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 9 && out[4] == 4 && out[5] == 10);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 9 && out[3] == 4 && out[4] == 3 && out[5] == 10);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 10 && out[5] == 9);
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
