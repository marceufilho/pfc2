/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_39.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long l[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotateRight(5, l, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 4 && out[1] == 5 && out[2] == 1 && out[3] == 2 && out[4] == 3);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 4);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 3 && out[1] == 4 && out[2] == 5 && out[3] == 1 && out[4] == 2);
}

static void test_case_1(void)
{
    static const long l[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotateRight(5, l, 7L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 4 && out[1] == 5 && out[2] == 1 && out[3] == 2 && out[4] == 3);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 4);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 3 && out[1] == 4 && out[2] == 5 && out[3] == 1 && out[4] == 2);
}

static void test_case_2(void)
{
    static const long l[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotateRight(5, l, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 5 && out[1] == 1 && out[2] == 2 && out[3] == 3 && out[4] == 4);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 4 && out[1] == 5 && out[2] == 1 && out[3] == 2 && out[4] == 3);
}

static void test_case_3(void)
{
    static const long l[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = rotateRight(0, l, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 42);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_case_0);
    RUN_TEST(test_case_1);
    RUN_TEST(test_case_2);
    RUN_TEST(test_case_3);
    return UNITY_END();
}
