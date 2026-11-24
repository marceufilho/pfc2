/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_89.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long s[] = {1L, 2L, 2L, 3L, 1L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = SetToSeq(5, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 3 && out[2] == 2);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 2 && out[3] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 2 && out[1] == 1 && out[2] == 3);
}

static void test_case_1(void)
{
    static const long s[] = {5L, 5L, 5L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = SetToSeq(4, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 5);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 5 && out[1] == 5);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 6);
}

static void test_case_2(void)
{
    static const long s[] = {0};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = SetToSeq(0, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 2);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
}

static void test_case_3(void)
{
    static const long s[] = {11L, 22L, 33L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = SetToSeq(3, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 11 && out[1] == 22 && out[2] == 33);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 33 && out[1] == 22 && out[2] == 11);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 11 && out[1] == 11 && out[2] == 22 && out[3] == 33);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 11 && out[1] == 33);
}

static void test_case_4(void)
{
    static const long s[] = {3L, 1L, 4L, 1L, 5L, 9L, 2L, 6L, 5L};
    long out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = SetToSeq(9, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 7 && out[0] == 3 && out[1] == 1 && out[2] == 4 && out[3] == 5 && out[4] == 9 && out[5] == 2 && out[6] == 6);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 3 && out[1] == 1 && out[2] == 4 && out[3] == 1 && out[4] == 5 && out[5] == 9 && out[6] == 2 && out[7] == 6 && out[8] == 5);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 1 && out[1] == 3 && out[2] == 4 && out[3] == 5 && out[4] == 9 && out[5] == 2 && out[6] == 6);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 3 && out[1] == 1 && out[2] == 4 && out[3] == 5 && out[4] == 9 && out[5] == 6);
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
