/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_72.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = append(3, a, 4L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 0);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 4 && out[3] == 3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 4 && out[1] == 1 && out[2] == 2 && out[3] == 3);
}

static void test_case_1(void)
{
    static const long a[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = append(0, a, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 0);
}

static void test_case_2(void)
{
    static const long a[] = {5L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = append(2, a, -1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 5 && out[1] == 6 && out[2] == -1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == -1 && out[2] == 6);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 6 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 6 && out[1] == 5 && out[2] == -1);
}

static void test_case_3(void)
{
    static const long a[] = {0L, 0L, 0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = append(3, a, 1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 1);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 0 && out[2] == 0 && out[3] == 0);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 1 && out[2] == 0 && out[3] == 0);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 0 && out[2] == 1 && out[3] == 0);
}

static void test_case_4(void)
{
    static const long a[] = {-2L, -3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = append(2, a, -4L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == -2 && out[1] == -3 && out[2] == -4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -2 && out[1] == -4 && out[2] == -3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -2 && out[1] == -3 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -3 && out[1] == -2 && out[2] == -4);
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
