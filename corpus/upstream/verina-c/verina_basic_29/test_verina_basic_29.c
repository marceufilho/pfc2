/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_29.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long s[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(5, s, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 4 && out[3] == 5);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 5);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 3 && out[2] == 4 && out[3] == 5);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 2 && out[1] == 3 && out[2] == 4 && out[3] == 5);
}

static void test_case_1(void)
{
    static const long s[] = {10L, 20L, 30L, 40L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(4, s, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 20 && out[1] == 30 && out[2] == 40);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 30 && out[2] == 40);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 10 && out[1] == 20 && out[2] == 30 && out[3] == 40);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 20 && out[1] == 30 && out[2] == 40 && out[3] == 0);
}

static void test_case_2(void)
{
    static const long s[] = {10L, 20L, 30L, 40L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(4, s, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 10 && out[1] == 20 && out[2] == 30);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 20 && out[1] == 30 && out[2] == 40);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 20 && out[2] == 40);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 10 && out[1] == 30 && out[2] == 40);
}

static void test_case_3(void)
{
    static const long s[] = {7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(1, s, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 7);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
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
