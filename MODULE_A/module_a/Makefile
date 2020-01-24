
MODULE_DIR = MODULE_A/module_a
PROJ_ROOT = ../../
#SRC_DIR = .

# Use some default settings for these variables only if they are not defined
# already by a module's Makefile
UNITY_DIR ?= $(PROJ_ROOT)unit_test/unity
FFF_DIR ?= $(PROJ_ROOT)unit_test/fff

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
SRC_FILES += $(wildcard $(UNITY_DIR)/*.c)

HDR_DIRS = $(HEADER_PATH)

# All places to look for headers
HDR_DIRS += $(UNITY_DIR)
HDR_DIRS += $(FFF_DIR)
INC_DIRS = $(addprefix -I, $(HDR_DIRS))

# List of all headers so we can track their existence as dependencies
INC_FILES= $(wildcard $(HDR_DIRS)/$(HEADER_GLOB))

# Special #defines desired for the build
SYMBOLS=

BUILD_DIRS = $(RESULT_PATH) $(BUILD_PATH) $(RUNNER_PATH)

TESTS_DIR = unit_testing/tests
RUNNER_DIR = unit_testing/runners
EXE_DIR = unit_testing/exe
RESULTS_DIR = unit_testing/results
RESULTS_TXT_PREFIX =
RESULTS_TXT_SUFFIX = _results
include $(PROJ_ROOT)/unit_test/module_makefile.mk
