/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_68.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char input[] = {97, 97, 97, 98, 98, 98, 99, 99};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(8, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 97 && out[1] == 51 && out[2] == 98 && out[3] == 51 && out[4] == 99 && out[5] == 50);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 97 && out[1] == 51 && out[2] == 98 && out[3] == 51);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 97 && out[1] == 51 && out[2] == 98 && out[3] == 51 && out[4] == 99 && out[5] == 50 && out[6] == 120);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 97 && out[1] == 98 && out[2] == 99);
}

static void test_case_1(void)
{
    static const char input[] = {33, 33, 33, 36, 36, 36, 37, 37, 37};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(9, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 6 && out[0] == 33 && out[1] == 51 && out[2] == 36 && out[3] == 51 && out[4] == 37 && out[5] == 51);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 33 && out[1] == 51 && out[2] == 36 && out[3] == 51 && out[4] == 37);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 33 && out[1] == 33 && out[2] == 33 && out[3] == 36 && out[4] == 36 && out[5] == 36 && out[6] == 37 && out[7] == 37);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 33 && out[1] == 51 && out[2] == 36 && out[3] == 51 && out[4] == 37 && out[5] == 52);
}

static void test_case_2(void)
{
    static const char input[] = {97, 97, 97, 97, 97};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(5, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 97 && out[1] == 53);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 97 && out[1] == 52);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 97 && out[1] == 54);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
}

static void test_case_3(void)
{
    static const char input[] = {97, 98, 99, 100};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(4, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 97 && out[1] == 49 && out[2] == 98 && out[3] == 49 && out[4] == 99 && out[5] == 49 && out[6] == 100 && out[7] == 49);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 97 && out[1] == 98 && out[2] == 99 && out[3] == 100);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 97 && out[1] == 49 && out[2] == 98 && out[3] == 49 && out[4] == 99 && out[5] == 49);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 97 && out[1] == 49 && out[2] == 98 && out[3] == 49 && out[4] == 99 && out[5] == 49 && out[6] == 100 && out[7] == 50);
}

static void test_case_4(void)
{
    static const char input[] = {0};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(0, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 97 && out[1] == 49);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 32);
}

static void test_case_5(void)
{
    static const char input[] = {65, 97, 65, 66, 98};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(5, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 10 && out[0] == 65 && out[1] == 49 && out[2] == 97 && out[3] == 49 && out[4] == 65 && out[5] == 49 && out[6] == 66 && out[7] == 49 && out[8] == 98 && out[9] == 49);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 65 && out[1] == 97 && out[2] == 65 && out[3] == 66 && out[4] == 98);
    TEST_ASSERT_FALSE(found == 8 && out[0] == 65 && out[1] == 49 && out[2] == 97 && out[3] == 49 && out[4] == 65 && out[5] == 49 && out[6] == 66 && out[7] == 49);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 65 && out[1] == 49 && out[2] == 97 && out[3] == 49 && out[4] == 65 && out[5] == 49 && out[6] == 66 && out[7] == 49 && out[8] == 98 && out[9] == 50);
}

static void test_case_6(void)
{
    static const char input[] = {119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(17, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 119 && out[1] == 49 && out[2] == 55);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 119 && out[1] == 49 && out[2] == 54);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 119 && out[1] == 49 && out[2] == 56);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 119);
}

static void test_case_7(void)
{
    static const char input[] = {97};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(1, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 97 && out[1] == 49);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 97);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 97 && out[1] == 50);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_8(void)
{
    static const char input[] = {32, 32};
    char out[64];
    for (int i = 0; i < 64; i++) { out[i] = 77; }
    long found = runLengthEncoder(2, input, 64, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 32 && out[1] == 50);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 32);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 32 && out[1] == 49);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 32 && out[1] == 51);
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
