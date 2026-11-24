/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_64.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long lst[] = {1L, 2L, 3L, 2L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(5, lst, 2L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 1 && out[1] == 3 && out[2] == 4);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 1 && out[1] == 2 && out[2] == 3 && out[3] == 4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 1 && out[1] == 4);
}

static void test_case_1(void)
{
    static const long lst[] = {5L, 5L, 5L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(4, lst, 5L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 5);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 5 && out[1] == 5);
}

static void test_case_2(void)
{
    static const long lst[] = {7L, 8L, 9L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(3, lst, 4L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 7 && out[1] == 8 && out[2] == 9);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 7 && out[1] == 8);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 8 && out[1] == 9);
}

static void test_case_3(void)
{
    static const long lst[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(0, lst, 3L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 3);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 0);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 2 && out[2] == 3);
}

static void test_case_4(void)
{
    static const long lst[] = {0L, 1L, 0L, 2L, 0L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = removeElement(5, lst, 0L, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 0 && out[1] == 1 && out[2] == 2);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 1 && out[1] == 0 && out[2] == 2);
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
