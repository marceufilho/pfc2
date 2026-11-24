/* Generated from the task's test.json by corpus/verina-notes/interface.py. Do not edit. */
#include "test-framework/unity.h"
#include "verina_advanced_57.h"

void setUp(void)
{
}

void tearDown(void)
{
}

static void test_case_0(void)
{
    static const long nums1[] = {4L, 1L, 2L};
    static const long nums2[] = {1L, 3L, 4L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(3, nums1, 4, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == -1 && out[1] == 3 && out[2] == -1);
    TEST_ASSERT_FALSE(found == 3 && out[0] == 3 && out[1] == -1 && out[2] == 3);
}

static void test_case_1(void)
{
    static const long nums1[] = {2L, 4L};
    static const long nums2[] = {1L, 2L, 3L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(2, nums1, 4, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 2 && out[0] == 3 && out[1] == -1);
    TEST_ASSERT_FALSE(found == 2 && out[0] == -1 && out[1] == 3);
}

static void test_case_2(void)
{
    static const long nums1[] = {1L};
    static const long nums2[] = {1L, 2L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(1, nums1, 2, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == 2);
    TEST_ASSERT_FALSE(found == 1 && out[0] == -1);
}

static void test_case_3(void)
{
    static const long nums1[] = {5L};
    static const long nums2[] = {5L, 4L, 3L, 2L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(1, nums1, 5, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 1 && out[0] == -1);
    TEST_ASSERT_FALSE(found == 1 && out[0] == 4);
}

static void test_case_4(void)
{
    static const long nums1[] = {1L, 3L, 5L, 2L, 4L};
    static const long nums2[] = {6L, 5L, 4L, 3L, 2L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(5, nums1, 6, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 5 && out[0] == -1 && out[1] == -1 && out[2] == -1 && out[3] == -1 && out[4] == -1);
    TEST_ASSERT_FALSE(found == 5 && out[0] == 6 && out[1] == 5 && out[2] == 6 && out[3] == 3 && out[4] == 6);
}

static void test_case_5(void)
{
    static const long nums1[] = {1L, 2L, 3L};
    static const long nums2[] = {3L, 2L, 1L, 4L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(3, nums1, 4, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 3 && out[0] == 4 && out[1] == 4 && out[2] == 4);
    TEST_ASSERT_FALSE(found == 3 && out[0] == -1 && out[1] == -1 && out[2] == -1);
}

static void test_case_6(void)
{
    static const long nums1[] = {4L, 3L, 2L, 1L};
    static const long nums2[] = {4L, 3L, 2L, 1L};
    long out[16];
    for (int i = 0; i < 16; i++) { out[i] = 77; }
    long found = nextGreaterElement(4, nums1, 4, nums2, 16, out);
    (void)found;
    TEST_ASSERT_TRUE(found == 4 && out[0] == -1 && out[1] == -1 && out[2] == -1 && out[3] == -1);
    TEST_ASSERT_FALSE(found == 4 && out[0] == 3 && out[1] == 2 && out[2] == 1 && out[3] == -1);
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
