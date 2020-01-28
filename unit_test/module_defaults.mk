
SOURCE_PATH = .
SOURCE_GLOB = *.c

HEADER_PATH = .
HEADER_GLOB = *.h

TEST_PATH = unit_testing/tests
TEST_GLOB = *_tests.c

RUNNER_PATH = unit_testing/runners
RUNNER_GLOB = test_*_runner.c

BUILD_PATH = unit_testing/exe
BUILD_PREFIX = test_
BUILD_SUFFIX =

RESULT_PATH = unit_testing/results
RESULT_PREFIX =
RESULT_SUFFIX = _results

# Complete list of all source files to be compiled for the build
SRC_FILES := $(wildcard $(SOURCE_PATH)/$(SOURCE_GLOB))
SRC_FILES += $(wildcard $(TEST_PATH)/$(TEST_GLOB))
SRC_FILES += $(wildcard $(RUNNER_PATH)/$(RUNNER_GLOB))

# This variable is started with our production code's header(s)
HDR_DIRS = $(HEADER_PATH)

# This starts a list of all the headers used in the build to describe a depency on them
INC_FILES = $(wildcard $(HDR_DIRS)/$(HEADER_GLOB))

# Make will build these directories if they do not yet exist
BUILD_DIRS = $(RESULT_PATH) $(BUILD_PATH) $(RUNNER_PATH)
