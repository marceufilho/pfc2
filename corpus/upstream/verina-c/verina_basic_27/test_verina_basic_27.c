/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_27.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {97, 98, 99, 97};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstRepeatedChar(4, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 97);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 98);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 99);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_1(void)
{
    static const char s[] = {97, 98, 99, 100, 101, 102};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstRepeatedChar(6, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 97);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 122);
}

static void test_case_2(void)
{
    static const char s[] = {97, 97, 98, 98, 99, 99};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstRepeatedChar(6, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 97);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 98);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 99);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_3(void)
{
    static const char s[] = {0};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstRepeatedChar(0, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 120);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 121);
}

static void test_case_4(void)
{
    static const char s[] = {97, 98, 98, 99};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstRepeatedChar(4, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 1 && out[1] == 98);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 97);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 99);
    TEST_ASSERT_FALSE(out[0] == 0);
}

static void test_case_5(void)
{
    static const char s[] = {65, 97};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = findFirstRepeatedChar(2, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(out[0] == 0);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 65);
    TEST_ASSERT_FALSE(out[0] == 1 && out[1] == 97);
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
    return UNITY_END();
}
