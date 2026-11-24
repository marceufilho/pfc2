/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_58.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long s[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = double_array_elements(0, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == -1);
}

static void test_case_1(void)
{
    static const long s[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = double_array_elements(5, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 2 && out[1] == 4 && out[2] == 6 && out[3] == 8 && out[4] == 10);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 2 && out[1] == 4 && out[2] == 6 && out[3] == 8 && out[4] == 9);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 0 && out[1] == 4 && out[2] == 6 && out[3] == 8 && out[4] == 10);
}

static void test_case_2(void)
{
    static const long s[] = {0L, -1L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = double_array_elements(3, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == -2 && out[2] == 10);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == -1 && out[2] == 5);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == -2 && out[2] == 10);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 10);
}

static void test_case_3(void)
{
    static const long s[] = {100L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = double_array_elements(1, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 200);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 100);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 201);
}

static void test_case_4(void)
{
    static const long s[] = {-3L, -4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = double_array_elements(2, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == -6 && out[1] == -8);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 3 && out[1] == -4);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -6 && out[1] == -7);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -6 && out[1] == -9);
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
