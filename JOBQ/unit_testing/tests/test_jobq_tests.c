/**********************************************************
| script_sandbox - test_jobq_tests.c
| Author: troyerta
| Date: 2019-12-04
| License: MIT
| Repository: https://gitlab.com/troyerta/simple_build_system
| Description:
**********************************************************/

/**********************************************************
| Includes
**********************************************************/
#include "unity_fixture.h"
#include <stdint.h>
#include "jobq_prv.h"
#include "JOBQ_pub.h"
#include <stdio.h>
#include <stdlib.h>

/**********************************************************
| Test Groups
**********************************************************/
TEST_GROUP( JOBQ_TEST_GROUP_A );

/**********************************************************
| Types
**********************************************************/

/**********************************************************
| Literal Constants
**********************************************************/

/**********************************************************
| Memory Constants
**********************************************************/

/**********************************************************
| Variables
**********************************************************/
LinkedList* list;
void* value = (void*)1;

/**********************************************************
| Macros
**********************************************************/

/**********************************************************
| Test Setup and Teardown
**********************************************************/
TEST_SETUP( JOBQ_TEST_GROUP_A )
{
    list = emlist_create();
}

TEST_TEAR_DOWN( JOBQ_TEST_GROUP_A )
{
    emlist_destroy(list);
}

/**********************************************************
| Tests
**********************************************************/
TEST( JOBQ_TEST_GROUP_A, test_init )
{
    TEST_ASSERT( list->head == NULL );
}

TEST( JOBQ_TEST_GROUP_A , test_insert )
{
    TEST_ASSERT( emlist_insert(list, value) );
    TEST_ASSERT( emlist_contains(list, value) );
}

TEST( JOBQ_TEST_GROUP_A, test_contains )
{
    emlist_insert(list, value);
    TEST_ASSERT(emlist_contains(list, value));
    TEST_ASSERT(!emlist_contains(list, (void*)2));
}

TEST( JOBQ_TEST_GROUP_A, test_remove )
{
    emlist_insert(list, value);
    TEST_ASSERT(emlist_contains(list, value));
    TEST_ASSERT(emlist_remove(list, value));
    TEST_ASSERT(!emlist_contains(list, value));
}

TEST( JOBQ_TEST_GROUP_A, test_remove_not_in_list )
{
    emlist_insert(list, value);
    TEST_ASSERT(emlist_contains(list, value));
    TEST_ASSERT(!emlist_remove(list, (void*)2));
    TEST_ASSERT(emlist_contains(list, value));
}

TEST( JOBQ_TEST_GROUP_A, test_is_empty )
{
    TEST_ASSERT(emlist_is_empty(list));
    emlist_insert(list, value);
    TEST_ASSERT(!emlist_is_empty(list));
}

TEST( JOBQ_TEST_GROUP_A, test_size )
{
    TEST_ASSERT_EQUAL_INT(0, emlist_size(list));
    emlist_insert(list, (void*)1);
    TEST_ASSERT_EQUAL_INT(1, emlist_size(list));
    emlist_insert(list, (void*)2);
    TEST_ASSERT_EQUAL_INT(2, emlist_size(list));
    emlist_insert(list, (void*)3);
    TEST_ASSERT_EQUAL_INT(3, emlist_size(list));
    emlist_remove(list, (void*)1);
    emlist_remove(list, (void*)2);
    emlist_remove(list, (void*)3);
    TEST_ASSERT_EQUAL_INT(0, emlist_size(list));
}

TEST( JOBQ_TEST_GROUP_A, test_create )
{
    LinkedList* heapList = emlist_create();
    TEST_ASSERT(heapList != NULL);
    emlist_destroy(heapList);
}
