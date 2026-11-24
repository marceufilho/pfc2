/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_2.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long s[] = {3L, 1L, 4L, 1L, 5L, 9L, 2L, 6L, 5L, 3L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(11, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_1(void)
{
    static const long s[] = {0L, 1L, 2L, 3L, 4L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(6, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_2(void)
{
    static const long s[] = {1L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(1, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_3(void)
{
    static const long s[] = {10L, 10L, 10L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(3, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 10);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 9);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_4(void)
{
    static const long s[] = {3L, 2L, 2L, 2L, 2L, 2L, 2L, 1L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(8, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_5(void)
{
    static const long s[] = {0L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(1, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_6(void)
{
    static const long s[] = {100L, 99L, 98L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(3, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 98);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 99);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 97);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_7(void)
{
    static const long s[] = {0};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = findSmallest(0, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
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
    RUN_TEST(test_case_7);
    return UNITY_END();
}
