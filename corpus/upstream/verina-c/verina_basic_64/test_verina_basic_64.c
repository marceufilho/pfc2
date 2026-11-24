/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_basic_64.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char oline[] = {97, 98, 99, 100, 101};
    static const char nl[] = {88, 89};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = insert(5, oline, 5L, 2, nl, 2L, 2L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 7 && out[0] == 97 && out[1] == 98 && out[2] == 88 && out[3] == 89 && out[4] == 99 && out[5] == 100 && out[6] == 101);
    TEST_ASSERT_FALSE(found == 6 && out[0] == 97 && out[1] == 98 && out[2] == 88 && out[3] == 89 && out[4] == 99 && out[5] == 100);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 97 && out[1] == 98 && out[2] == 88 && out[3] == 89 && out[4] == 99 && out[5] == 100 && out[6] == 102);
    TEST_ASSERT_FALSE(found == 7 && out[0] == 97 && out[1] == 88 && out[2] == 98 && out[3] == 89 && out[4] == 99 && out[5] == 100 && out[6] == 101);
}

static void test_case_1(void)
{
    static const char oline[] = {72, 101, 108, 108, 111};
    static const char nl[] = {87, 111, 114, 108, 100};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = insert(5, oline, 5L, 5, nl, 5L, 0L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 10 && out[0] == 87 && out[1] == 111 && out[2] == 114 && out[3] == 108 && out[4] == 100 && out[5] == 72 && out[6] == 101 && out[7] == 108 && out[8] == 108 && out[9] == 111);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 72 && out[1] == 101 && out[2] == 108 && out[3] == 108 && out[4] == 111 && out[5] == 87 && out[6] == 111 && out[7] == 114 && out[8] == 108 && out[9] == 100);
    TEST_ASSERT_FALSE(found == 11 && out[0] == 87 && out[1] == 111 && out[2] == 114 && out[3] == 108 && out[4] == 100 && out[5] == 72 && out[6] == 101 && out[7] == 108 && out[8] == 108 && out[9] == 111 && out[10] == 33);
    TEST_ASSERT_FALSE(found == 10 && out[0] == 87 && out[1] == 111 && out[2] == 114 && out[3] == 108 && out[4] == 100 && out[5] == 87 && out[6] == 111 && out[7] == 114 && out[8] == 108 && out[9] == 100);
}

static void test_case_2(void)
{
    static const char oline[] = {76, 101, 97, 110};
    static const char nl[] = {52};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = insert(4, oline, 4L, 1, nl, 1L, 4L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 76 && out[1] == 101 && out[2] == 97 && out[3] == 110 && out[4] == 52);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 76 && out[1] == 101 && out[2] == 97 && out[3] == 110);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 76 && out[1] == 101 && out[2] == 97 && out[3] == 110 && out[4] == 32);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 52 && out[1] == 76 && out[2] == 101 && out[3] == 97 && out[4] == 110);
}

static void test_case_3(void)
{
    static const char oline[] = {84, 101, 115, 116};
    static const char nl[] = {0};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = insert(4, oline, 4L, 0, nl, 0L, 2L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 84 && out[1] == 101 && out[2] == 115 && out[3] == 116);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 84 && out[1] == 101 && out[2] == 115);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 84 && out[1] == 115 && out[2] == 116 && out[3] == 101);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 116 && out[1] == 101 && out[2] == 115 && out[3] == 84);
}

static void test_case_4(void)
{
    static const char oline[] = {49, 50, 51, 52, 53, 54};
    static const char nl[] = {97, 98, 99};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = insert(6, oline, 5L, 3, nl, 3L, 3L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 8 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 97 && out[4] == 98 && out[5] == 99 && out[6] == 52 && out[7] == 53);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 97 && out[4] == 98 && out[5] == 99 && out[6] == 52 && out[7] == 53 && out[8] == 54);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 52 && out[4] == 97 && out[5] == 98 && out[6] == 99 && out[7] == 53 && out[8] == 54);
    TEST_ASSERT_FALSE(found == 9 && out[0] == 49 && out[1] == 50 && out[2] == 51 && out[3] == 97 && out[4] == 98 && out[5] == 52 && out[6] == 99 && out[7] == 53 && out[8] == 54);
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
