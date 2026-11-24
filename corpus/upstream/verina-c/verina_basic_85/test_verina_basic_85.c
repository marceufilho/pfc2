/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_85.h"

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
    long found = reverse(5, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 5 && out[1] == 4 && out[2] == 3 && out[3] == 2 && out[4] == 1);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 3 && out[2] == 4 && out[3] == 2 && out[4] == 1);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 2 && out[1] == 3 && out[2] == 4 && out[3] == 5 && out[4] == 6);
}

static void test_case_1(void)
{
    static const long a[] = {10L, 20L, 30L, 40L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverse(4, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 40 && out[1] == 30 && out[2] == 20 && out[3] == 10);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 40 && out[1] == 20 && out[2] == 30 && out[3] == 10);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 30 && out[1] == 20 && out[2] == 10 && out[3] == 40);
}

static void test_case_2(void)
{
    static const long a[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverse(0, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == -1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
}

static void test_case_3(void)
{
    static const long a[] = {7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverse(1, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 7);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 7 && out[1] == 7);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
}

static void test_case_4(void)
{
    static const long a[] = {-1L, 0L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverse(3, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == -1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -1 && out[1] == 0 && out[2] == 1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 1 && out[2] == -1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == -1 && out[2] == 0);
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
