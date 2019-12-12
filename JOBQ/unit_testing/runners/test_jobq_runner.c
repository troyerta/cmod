#include "unity_fixture.h"

TEST_GROUP_RUNNER( JOBQ_TEST_GROUP_A )
{
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_init );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_insert );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_contains );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_remove );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_remove_not_in_list );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_is_empty );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_size );
RUN_TEST_CASE( JOBQ_TEST_GROUP_A, test_create );
}

static void RunAllTests( void )
{
RUN_TEST_GROUP( JOBQ_TEST_GROUP_A );
}

int main( int argc, const char * argv[] )
{
return UnityMain( argc, argv, RunAllTests );
}

