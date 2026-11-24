/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_14.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    long found = ifPowerOfFour(0L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_1(void)
{
    long found = ifPowerOfFour(1L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_2(void)
{
    long found = ifPowerOfFour(2L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_3(void)
{
    long found = ifPowerOfFour(3L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_4(void)
{
    long found = ifPowerOfFour(4L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_5(void)
{
    long found = ifPowerOfFour(8L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_6(void)
{
    long found = ifPowerOfFour(16L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_7(void)
{
    long found = ifPowerOfFour(64L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_8(void)
{
    long found = ifPowerOfFour(95L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_9(void)
{
    long found = ifPowerOfFour(100L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_10(void)
{
    long found = ifPowerOfFour(256L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
    TEST_ASSERT_FALSE(found == 0);
}

static void test_case_11(void)
{
    long found = ifPowerOfFour(520L);
    (void)found;
    TEST_ASSERT_TRUE(found == 0);
    TEST_ASSERT_FALSE(found == 1);
}

static void test_case_12(void)
{
    long found = ifPowerOfFour(1024L);
    (void)found;
    TEST_ASSERT_TRUE(found == 1);
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
    RUN_TEST(test_case_9);
    RUN_TEST(test_case_10);
    RUN_TEST(test_case_11);
    RUN_TEST(test_case_12);
    return UNITY_END();
}
