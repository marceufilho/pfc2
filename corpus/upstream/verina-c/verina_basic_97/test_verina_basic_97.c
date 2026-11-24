/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_97.h"

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
    long found = TestArrayElements(5, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 60 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 1 && out[1] == 60 && out[2] == 3 && out[3] == 4 && out[4] == 5);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 1 && out[1] == 2 && out[2] == 60 && out[3] == 4 && out[4] == 5 && out[5] == 0);
}

static void test_case_1(void)
{
    static const long a[] = {60L, 30L, 20L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = TestArrayElements(3, a, 1L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 60 && out[1] == 60 && out[2] == 20);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 60 && out[1] == 30 && out[2] == 20);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 60 && out[1] == 30 && out[2] == 60);
}

static void test_case_2(void)
{
    static const long a[] = {10L, 20L, 30L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = TestArrayElements(3, a, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 60 && out[1] == 20 && out[2] == 30);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 20 && out[2] == 30);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 60 && out[2] == 30);
}

static void test_case_3(void)
{
    static const long a[] = {5L, 10L, 15L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = TestArrayElements(3, a, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 5 && out[1] == 10 && out[2] == 60);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 10 && out[2] == 15);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 5 && out[1] == 60 && out[2] == 15);
}

static void test_case_4(void)
{
    static const long a[] = {0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = TestArrayElements(1, a, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 60);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 70);
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
