/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_5.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long l1[] = {2L, 4L, 3L};
    static const long l2[] = {5L, 6L, 4L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = addTwoNumbers(3, l1, 3, l2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 7 && out[1] == 0 && out[2] == 8);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 4 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
}

static void test_case_1(void)
{
    static const long l1[] = {0L};
    static const long l2[] = {0L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = addTwoNumbers(1, l1, 1, l2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 0);
}

static void test_case_2(void)
{
    static const long l1[] = {9L, 9L, 9L, 9L, 9L, 9L, 9L};
    static const long l2[] = {9L, 9L, 9L, 9L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = addTwoNumbers(7, l1, 4, l2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 8 && out[1] == 9 && out[2] == 9 && out[3] == 9 && out[4] == 0 && out[5] == 0 && out[6] == 0 && out[7] == 1);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 9 && out[1] == 9 && out[2] == 9 && out[3] == 9 && out[4] == 9 && out[5] == 9 && out[6] == 9 && out[7] == 9);
}

static void test_case_3(void)
{
    static const long l1[] = {1L, 2L, 3L};
    static const long l2[] = {4L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = addTwoNumbers(3, l1, 2, l2, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 5 && out[1] == 7 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 5 && out[1] == 7);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 7 && out[2] == 4);
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
