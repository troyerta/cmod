#include "unity_fixture.h"

TEST_GROUP_RUNNER( LedDriver )
{
RUN_TEST_CASE( LedDriver, LedsOffAfterCreate );
RUN_TEST_CASE( LedDriver, TurnOnLedOne );
RUN_TEST_CASE( LedDriver, TurnOffLedOne );
RUN_TEST_CASE( LedDriver, TurnOnMultipleLeds );
RUN_TEST_CASE( LedDriver, TurnOffMultipleLeds );
RUN_TEST_CASE( LedDriver, TurnOffAnyLed );
RUN_TEST_CASE( LedDriver, LedMemoryIsNotReadable );
RUN_TEST_CASE( LedDriver, UpperAndLowerBounds );
RUN_TEST_CASE( LedDriver, OutOfBoundsTurnOnDoesNoHarm );
RUN_TEST_CASE( LedDriver, OutOfBoundsTurnOffDoesNoHarm );
RUN_TEST_CASE( LedDriver, OutOfBoundsProducesRuntimeError );
RUN_TEST_CASE( LedDriver, IsOn );
RUN_TEST_CASE( LedDriver, IsOff );
RUN_TEST_CASE( LedDriver, OutOfBoundsLedsAreAlwaysOff );
}

TEST_GROUP_RUNNER( LedDriver2 )
{
RUN_TEST_CASE( LedDriver2, AllOn );
RUN_TEST_CASE( LedDriver2, AllOff );
}

TEST_GROUP_RUNNER( ProductionCode )
{
RUN_TEST_CASE( ProductionCode, FindFunction_WhichIsBroken_ShouldReturnZeroIfItemIsNotInList_WhichWorksEvenInOurBrokenCode );
RUN_TEST_CASE( ProductionCode, FindFunction_WhichIsBroken_ShouldReturnTheIndexForItemsInList_WhichWillFailBecauseOurFunctionUnderTestIsBroken );
RUN_TEST_CASE( ProductionCode, FunctionWhichReturnsLocalVariable_ShouldReturnTheCurrentCounterValue );
RUN_TEST_CASE( ProductionCode, FunctionWhichReturnsLocalVariable_ShouldReturnTheCurrentCounterValueAgain );
RUN_TEST_CASE( ProductionCode, FnRetsLocVar_ShouldReturnCurrentCounter_FailsBCItsTestIsFlawed );
}

TEST_GROUP_RUNNER( ProductionCode2 )
{
RUN_TEST_CASE( ProductionCode2, IgnoredTest );
RUN_TEST_CASE( ProductionCode2, AnotherIgnoredTest );
RUN_TEST_CASE( ProductionCode2, ThisFunctionHasNotBeenTested_NeedsToBeImplemented );
}

static void RunAllTests( void )
{
RUN_TEST_GROUP( LedDriver );
RUN_TEST_GROUP( LedDriver2 );
RUN_TEST_GROUP( ProductionCode );
RUN_TEST_GROUP( ProductionCode2 );
}

int main( int argc, const char * argv[] )
{
return UnityMain( argc, argv, RunAllTests );
}

