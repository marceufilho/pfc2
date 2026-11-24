/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_88.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = ToArray(3, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 3 && out[1] == 2 && out[2] == 1);
}

static void test_case_1(void)
{
    static const long xs[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = ToArray(0, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 1 && out[1] == 0);
}

static void test_case_2(void)
{
    static const long xs[] = {0L, -1L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = ToArray(3, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == -1 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -1 && out[1] == 0 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == -1 && out[2] == 4);
}

static void test_case_3(void)
{
    static const long xs[] = {7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = ToArray(1, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 7);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 7);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 8);
}

static void test_case_4(void)
{
    static const long xs[] = {100L, 200L, 300L, 400L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = ToArray(4, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 100 && out[1] == 200 && out[2] == 300 && out[3] == 400);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 100 && out[1] == 200 && out[2] == 300);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 100 && out[1] == 300 && out[2] == 200 && out[3] == 400);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 400 && out[1] == 300 && out[2] == 200 && out[3] == 100);
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
