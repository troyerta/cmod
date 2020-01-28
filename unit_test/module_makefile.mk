# ==========================================
#   Unity Project - A Test Framework for C
#   Copyright (c) 2007 Mike Karlesky, Mark VanderVoord, Greg Williams
#   [Released under MIT License. Please refer to license.txt for details]
# ==========================================

# We try to detect the OS we are running on, and adjust commands as needed
ifeq ($(OS),Windows_NT)
  ifeq ($(shell uname -s),) # not in a bash-like shell
	CLEANUP = del /F /Q
	MKDIR = mkdir
  else # in a bash-like shell, like msys
	CLEANUP = rm -f
	MKDIR = mkdir -p
  endif
	TARGET_EXTENSION=.exe
else
	CLEANUP = rm -f
	MKDIR = mkdir -p
	TARGET_EXTENSION=.out
endif

# We are not generating files called 'clean', 'help', or 'test'
.PHONY: clean
.PHONY: help
.PHONY: test

# The host PC compiler will eventually be configurable
C_COMPILER=gcc

# Specify your default build flags
CFLAGS=-std=c99
CFLAGS += -Wall
CFLAGS += -Wpointer-arith
CFLAGS += -Wcast-align
CFLAGS += -Wwrite-strings
CFLAGS += -Wswitch-default
CFLAGS += -Wunreachable-code
CFLAGS += -Winit-self
CFLAGS += -Wmissing-field-initializers
CFLAGS += -Wno-unknown-pragmas
CFLAGS += -Wundef

# Use some default settings for these variables only if they are not defined
# already by a module's Makefile
UNITY_DIR ?= $(PROJ_ROOT)unit_test/unity
FFF_DIR ?= $(PROJ_ROOT)unit_test/fff

# The executable's file name is generated from the runner source's name
EXECUTABLE = $(BUILD_PATH)/$(BUILD_PREFIX)$(notdir $(MODULE_DIR)$(BUILD_SUFFIX))$(TARGET_EXTENSION)

# The result's file name is generated from the runner source's name
RESULTS = $(RESULT_PATH)/$(RESULT_PREFIX)$(notdir $(MODULE_DIR))$(RESULT_SUFFIX).txt

SRC_FILES += $(wildcard $(UNITY_DIR)/*.c)

# Add the test harness dirs
HDR_DIRS += $(UNITY_DIR)
HDR_DIRS += $(FFF_DIR)

# Make the include dir string for call to the compiler
INC_DIRS = $(addprefix -I, $(HDR_DIRS))

# Add test harness headers to list of dependencies
INC_FILES += $(wildcard $(UNITY_DIR)/*.h)

# Special #defines desired for the build
SYMBOLS=

# Clean out old results and executable
# Then make sure all necessary directories are in place
# Then run the executable, piping output to our results file
test: clean $(BUILD_DIRS) $(RESULTS)

# After the executable is made, run it and pipe the stdout to the results file
# Return true to keep make from worrying
$(RESULTS): $(EXECUTABLE)
	@-./$< > $@; true

# Compile and link our tet program together using all our resources
# Test suite source and test runner must exist by this time, or the build will fail
$(EXECUTABLE): $(SRC_FILES) $(INC_FILES)
#	@echo $@
#	@echo $(SRC_DIRS)
#	@echo $(SRC_FILES)
#	@echo $(HDR_DIRS)
#	@echo $(INC_FILES)
#	@echo $(INC_DIRS)
#	@echo $(BUILD_DIRS)
	@$(C_COMPILER) $(CFLAGS) $(INC_DIRS) $(SYMBOLS) $(SRC_FILES) -o $(EXECUTABLE)

# Rules to make any module directories that hold generated files
$(BUILD_PATH):
	@$(MKDIR) $@

$(RUNNER_PATH):
	@$(MKDIR) $@

$(RESULT_PATH):
	@$(MKDIR) $@

# Delete old results file and executable to force compilation of sources under test
clean:
	@$(CLEANUP) $(BUILD_PATH)/*$(TARGET_EXTENSION)
	@$(CLEANUP) $(RESULT_PATH)/*.txt

# Adjust the width of the first column by changing the 30 value in the printf pattern to something larger or smaller
# Remove the | sort to have targets ordered the way they appear in the makefile instead of alphabetically
# Stolen from the internet
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Don't delete these files as if they were only intermediate artifacts of the build process
.PRECIOUS: $(EXECUTABLE)
.PRECIOUS: $(RESULTS)
