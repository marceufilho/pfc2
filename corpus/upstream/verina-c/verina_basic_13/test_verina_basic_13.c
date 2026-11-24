/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_13.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long a[] = {1L, 2L, 3L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = cubeElements(4, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 1 && out[1] == 8 && out[2] == 27 && out[3] == 64);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 4 && out[2] == 9 && out[3] == 16);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 8 && out[2] == 27 && out[3] == 63);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 0 && out[2] == 0 && out[3] == 0);
}

static void test_case_1(void)
{
    static const long a[] = {0L, -1L, -2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = cubeElements(4, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 0 && out[1] == -1 && out[2] == -8 && out[3] == 27);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 1 && out[2] == 8 && out[3] == -27);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == -1 && out[2] == -8 && out[3] == 26);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == -1 && out[2] == -8 && out[3] == 27);
}

static void test_case_2(void)
{
    static const long a[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = cubeElements(0, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == -1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
}

static void test_case_3(void)
{
    static const long a[] = {5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = cubeElements(1, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 125);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 5);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 25);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
}

static void test_case_4(void)
{
    static const long a[] = {-3L, -3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = cubeElements(2, a, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == -27 && out[1] == -27);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 27 && out[1] == 27);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -9 && out[1] == -9);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -27 && out[1] == 27);
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
