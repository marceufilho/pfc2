/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_105.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L};
    static const long b[] = {4L, 5L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = arrayProduct(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 4 && out[1] == 10 && out[2] == 18);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 4 && out[1] == 10 && out[2] == 17);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 10 && out[2] == 18);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 4 && out[1] == 10 && out[2] == 20);
}

static void test_case_1(void)
{
    static const long a[] = {0L, 0L, 0L};
    static const long b[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = arrayProduct(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 1 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 1);
}

static void test_case_2(void)
{
    static const long a[] = {-1L, 2L, -3L};
    static const long b[] = {3L, -4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = arrayProduct(3, a, 3, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == -3 && out[1] == -8 && out[2] == -15);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -3 && out[1] == -8 && out[2] == -14);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -3 && out[1] == -7 && out[2] == -15);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -2 && out[1] == -8 && out[2] == -15);
}

static void test_case_3(void)
{
    static const long a[] = {2L};
    static const long b[] = {10L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = arrayProduct(1, a, 1, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 20);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 10);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 30);
}

static void test_case_4(void)
{
    static const long a[] = {1L, 2L, 3L, 4L};
    static const long b[] = {2L, 2L, 2L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = arrayProduct(4, a, 4, b, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 2 && out[1] == 4 && out[2] == 6 && out[3] == 8);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 4 && out[2] == 6 && out[3] == 9);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 4 && out[2] == 6 && out[3] == 8);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 5 && out[2] == 6 && out[3] == 8);
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
