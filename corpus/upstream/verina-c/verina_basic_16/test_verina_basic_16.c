/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_16.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {104, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(13, s, 44L, 59L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 59 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 12 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 32 && out[6] == 119 && out[7] == 111 && out[8] == 114 && out[9] == 108 && out[10] == 100 && out[11] == 33);
    TEST_ASSERT_FALSE(found == 12 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 59 && out[6] == 119 && out[7] == 111 && out[8] == 114 && out[9] == 108 && out[10] == 100 && out[11] == 33);
}

static void test_case_1(void)
{
    static const char s[] = {97, 44, 98, 46, 99};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(5, s, 44L, 58L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 97 && out[1] == 58 && out[2] == 98 && out[3] == 46 && out[4] == 99);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 97 && out[1] == 44 && out[2] == 98 && out[3] == 46 && out[4] == 99);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 97 && out[1] == 59 && out[2] == 98 && out[3] == 46 && out[4] == 99);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 97 && out[1] == 98 && out[2] == 58 && out[3] == 99);
}

static void test_case_2(void)
{
    static const char s[] = {104, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(13, s, 111L, 79L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 79 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 79 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 79 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 79 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
}

static void test_case_3(void)
{
    static const char s[] = {0};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(0, s, 120L, 121L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 32);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
}

static void test_case_4(void)
{
    static const char s[] = {116, 101, 115, 116};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(4, s, 120L, 121L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 116 && out[1] == 101 && out[2] == 115 && out[3] == 116);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 116 && out[1] == 101 && out[2] == 115 && out[3] == 116 && out[4] == 121);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 116 && out[1] == 115 && out[2] == 101 && out[3] == 116);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 121 && out[1] == 120 && out[2] == 101 && out[3] == 115 && out[4] == 116);
}

static void test_case_5(void)
{
    static const char s[] = {117, 110, 99, 104, 97, 110, 103, 101, 100};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(9, s, 117L, 117L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 9 && out[0] == 117 && out[1] == 110 && out[2] == 99 && out[3] == 104 && out[4] == 97 && out[5] == 110 && out[6] == 103 && out[7] == 101 && out[8] == 100);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 110 && out[1] == 99 && out[2] == 104 && out[3] == 97 && out[4] == 110 && out[5] == 103 && out[6] == 101 && out[7] == 100);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 117 && out[1] == 110 && out[2] == 99 && out[3] == 104 && out[4] == 97 && out[5] == 110 && out[6] == 103 && out[7] == 101 && out[8] == 100 && out[9] == 33);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 117 && out[1] == 110 && out[2] == 99 && out[3] == 104 && out[4] == 97 && out[5] == 110 && out[6] == 103 && out[7] == 69 && out[8] == 100);
}

static void test_case_6(void)
{
    static const char s[] = {97, 97, 97};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = replaceChars(3, s, 97L, 98L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 98 && out[1] == 98 && out[2] == 98);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 97 && out[2] == 97);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 98);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 98 && out[1] == 98 && out[2] == 97);
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
    return UNITY_END();
}
