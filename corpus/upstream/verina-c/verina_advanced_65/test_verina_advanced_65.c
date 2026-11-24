/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_65.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {104, 101, 108, 108, 111};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverseString(5, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 111 && out[1] == 108 && out[2] == 108 && out[3] == 101 && out[4] == 104);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 111);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108);
}

static void test_case_1(void)
{
    static const char s[] = {97};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverseString(1, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 97);
    TEST_ASSERT_FALSE(found == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 97 && out[1] == 97);
}

static void test_case_2(void)
{
    static const char s[] = {0};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverseString(0, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 32);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
}

static void test_case_3(void)
{
    static const char s[] = {114, 97, 99, 101, 99, 97, 114};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverseString(7, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 7 && out[0] == 114 && out[1] == 97 && out[2] == 99 && out[3] == 101 && out[4] == 99 && out[5] == 97 && out[6] == 114);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 114 && out[1] == 99 && out[2] == 101 && out[3] == 97 && out[4] == 99 && out[5] == 97 && out[6] == 114);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 114 && out[1] == 97 && out[2] == 101 && out[3] == 99 && out[4] == 99 && out[5] == 97 && out[6] == 114);
}

static void test_case_4(void)
{
    static const char s[] = {76, 101, 97, 110};
    char out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = reverseString(4, s, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 110 && out[1] == 97 && out[2] == 101 && out[3] == 76);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 76 && out[1] == 101 && out[2] == 97 && out[3] == 110);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 97 && out[1] == 101 && out[2] == 110 && out[3] == 76);
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
