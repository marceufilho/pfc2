/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_56.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long xs[] = {0L, 1L, 0L, 3L, 12L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(5, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 3 && out[2] == 12 && out[3] == 0 && out[4] == 0);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 0 && out[1] == 1 && out[2] == 3 && out[3] == 12 && out[4] == 0);
}

static void test_case_1(void)
{
    static const long xs[] = {0L, 0L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(3, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 1 && out[2] == 0);
}

static void test_case_2(void)
{
    static const long xs[] = {1L, 2L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(3, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 3 && out[2] == 2);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 1 && out[2] == 2 && out[3] == 3);
}

static void test_case_3(void)
{
    static const long xs[] = {0L, 0L, 0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(3, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 0 && out[1] == 0 && out[2] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 0);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
}

static void test_case_4(void)
{
    static const long xs[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(0, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
}

static void test_case_5(void)
{
    static const long xs[] = {4L, 0L, 5L, 0L, 6L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(5, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 4 && out[1] == 5 && out[2] == 6 && out[3] == 0 && out[4] == 0);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 0 && out[1] == 4 && out[2] == 5 && out[3] == 6 && out[4] == 0);
}

static void test_case_6(void)
{
    static const long xs[] = {0L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(2, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 1);
}

static void test_case_7(void)
{
    static const long xs[] = {1L, 0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(2, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 0 && out[1] == 1);
}

static void test_case_8(void)
{
    static const long xs[] = {2L, 0L, 0L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = moveZeroes(4, xs, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 2 && out[1] == 3 && out[2] == 0 && out[3] == 0);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 0 && out[1] == 0 && out[2] == 2 && out[3] == 3);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 0 && out[2] == 3 && out[3] == 0);
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
    RUN_TEST(test_case_8);
    return UNITY_END();
}
