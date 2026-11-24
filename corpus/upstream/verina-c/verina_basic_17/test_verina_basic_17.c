/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_17.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 33};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = toLowercase(13, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 72 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 32 && out[7] == 119 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 72 && out[1] == 69 && out[2] == 76 && out[3] == 76 && out[4] == 79 && out[5] == 44 && out[6] == 32 && out[7] == 87 && out[8] == 79 && out[9] == 82 && out[10] == 76 && out[11] == 68 && out[12] == 33);
    TEST_ASSERT_FALSE(found == 13 && out[0] == 104 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 44 && out[6] == 32 && out[7] == 87 && out[8] == 111 && out[9] == 114 && out[10] == 108 && out[11] == 100 && out[12] == 33);
}

static void test_case_1(void)
{
    static const char s[] = {65, 66, 67};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = toLowercase(3, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 65 && out[1] == 66 && out[2] == 67);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 65 && out[1] == 98 && out[2] == 99);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 66 && out[2] == 67);
}

static void test_case_2(void)
{
    static const char s[] = {97, 98, 99};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = toLowercase(3, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 65 && out[1] == 66 && out[2] == 67);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 66 && out[2] == 99);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 67);
}

static void test_case_3(void)
{
    static const char s[] = {0};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = toLowercase(0, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 32);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 101 && out[1] == 109 && out[2] == 112 && out[3] == 116 && out[4] == 121);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 110 && out[1] == 117 && out[2] == 108 && out[3] == 108);
}

static void test_case_4(void)
{
    static const char s[] = {49, 50, 51, 52, 33, 64};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = toLowercase(6, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 52 && out[4] == 33 && out[5] == 64);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 52 && out[4] == 33 && out[5] == 35);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 52 && out[4] == 53 && out[5] == 33 && out[6] == 64);
}

static void test_case_5(void)
{
    static const char s[] = {77, 105, 120, 101, 100, 67, 65, 83, 69, 49, 50, 51};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = toLowercase(12, s, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 12 && out[0] == 109 && out[1] == 105 && out[2] == 120 && out[3] == 101 && out[4] == 100 && out[5] == 99 && out[6] == 97 && out[7] == 115 && out[8] == 101 && out[9] == 49 && out[10] == 50 && out[11] == 51);
    TEST_ASSERT_FALSE(found == 12 && out[0] == 77 && out[1] == 105 && out[2] == 120 && out[3] == 101 && out[4] == 100 && out[5] == 99 && out[6] == 97 && out[7] == 115 && out[8] == 101 && out[9] == 49 && out[10] == 50 && out[11] == 51);
    TEST_ASSERT_FALSE(found == 12 && out[0] == 109 && out[1] == 105 && out[2] == 120 && out[3] == 101 && out[4] == 100 && out[5] == 67 && out[6] == 65 && out[7] == 83 && out[8] == 69 && out[9] == 49 && out[10] == 50 && out[11] == 51);
    TEST_ASSERT_FALSE(found == 12 && out[0] == 77 && out[1] == 73 && out[2] == 88 && out[3] == 69 && out[4] == 68 && out[5] == 67 && out[6] == 65 && out[7] == 83 && out[8] == 69 && out[9] == 49 && out[10] == 50 && out[11] == 51);
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
