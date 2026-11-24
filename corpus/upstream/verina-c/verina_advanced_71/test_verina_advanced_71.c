/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_71.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const char s[] = {49, 48, 48, 48, 49, 49, 48, 48, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(9, s, 3L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == 49 && out[1] == 49 && out[2] == 48 && out[3] == 48 && out[4] == 49);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 48 && out[1] == 48 && out[2] == 48 && out[3] == 49 && out[4] == 49);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 49 && out[1] == 48 && out[2] == 48 && out[3] == 48 && out[4] == 49);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_1(void)
{
    static const char s[] = {49, 48, 49, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(4, s, 2L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 49 && out[1] == 49);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 49 && out[1] == 48 && out[2] == 49);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 48 && out[1] == 49);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    static const char s[] = {48, 48, 48};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(3, s, 1L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 48);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 48 && out[1] == 48);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 48 && out[1] == 48 && out[2] == 48);
}

static void test_case_3(void)
{
    static const char s[] = {49, 49, 49, 49, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(5, s, 3L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 49 && out[1] == 49 && out[2] == 49);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 49 && out[1] == 49);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 49 && out[1] == 49 && out[2] == 49 && out[3] == 49);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_4(void)
{
    static const char s[] = {49, 48, 49, 48, 48, 49, 48, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(8, s, 2L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 49 && out[1] == 48 && out[2] == 49);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 48 && out[1] == 49 && out[2] == 48);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 49 && out[1] == 48 && out[2] == 48 && out[3] == 49);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 48 && out[1] == 49 && out[2] == 48 && out[3] == 49);
}

static void test_case_5(void)
{
    static const char s[] = {49, 48, 48, 49, 48, 48, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(7, s, 2L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 49 && out[1] == 48 && out[2] == 48 && out[3] == 49);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 48 && out[1] == 48 && out[2] == 49 && out[3] == 48);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 48 && out[1] == 49 && out[2] == 48 && out[3] == 48);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 48 && out[1] == 48 && out[2] == 49);
}

static void test_case_6(void)
{
    static const char s[] = {49, 48, 48, 49, 48, 48, 48, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(8, s, 1L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 49);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 49 && out[1] == 48);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 49 && out[1] == 48 && out[2] == 48);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 48 && out[1] == 48 && out[2] == 48);
}

static void test_case_7(void)
{
    static const char s[] = {49, 48, 48, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(4, s, 0L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 48);
    TEST_ASSERT_FALSE(found == 2 && out[0] == 49 && out[1] == 48);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 49 && out[1] == 48 && out[2] == 48);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 49);
}

static void test_case_8(void)
{
    static const char s[] = {49, 49, 48, 49, 49};
    char out[32];
    for (int i = 0; i < 32; i++) { out[i] = 77; }
    long found = shortestBeautifulSubstring(5, s, 3L, 32, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == 49 && out[1] == 48 && out[2] == 49 && out[3] == 49);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 49 && out[1] == 49 && out[2] == 48 && out[3] == 49);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 49 && out[1] == 49 && out[2] == 48 && out[3] == 49 && out[4] == 49);
    TEST_ASSERT_FALSE(found == 0);
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
