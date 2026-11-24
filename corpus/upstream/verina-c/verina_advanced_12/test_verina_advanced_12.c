/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_12.h"

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
    long found = firstDuplicate(5, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_1(void)
{
    static const long lst[] = {5L, 1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(6, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 5);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_2(void)
{
    static const long lst[] = {1L, 2L, 3L, 4L, 5L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(5, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 3);
}

static void test_case_3(void)
{
    static const long lst[] = {7L, 7L, 7L, 7L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(4, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 7);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_4(void)
{
    static const long lst[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(0, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
}

static void test_case_5(void)
{
    static const long lst[] = {-1L, 2L, -1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(3, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == -1);
    TEST_ASSERT_FALSE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 2);
}

static void test_case_6(void)
{
    static const long lst[] = {1L, 2L, 2L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(4, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 2);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_7(void)
{
    static const long lst[] = {3L, 1L, 2L, 1L, 3L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = firstDuplicate(5, lst, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 1);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 3);
    TEST_ASSERT_FALSE(out[0] == 0);
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
    return UNITY_END();
}
