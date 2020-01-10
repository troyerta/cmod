# Adjust output for the OS we're on
ifeq ($(OS),Windows_NT)
  ifeq ($(shell uname -s),)
	CLEANUP = del /F /Q
	MKDIR = mkdir
  else
	CLEANUP = rm -f
	MKDIR = mkdir -p
  endif
	TARGET_EXTENSION=.exe
else
	CLEANUP = rm -f
	MKDIR = mkdir -p
	TARGET_EXTENSION=.out
endif

# We are not generating a file called 'clean'
.PHONY: clean
.PHONY: default

# Change this to your compiler if you don't have GCC
C_COMPILER=gcc

# Use some default settings for these variables only if they are not defined
# already by a module's Makefile
PROJ_ROOT ?= .
MAIN_DIR ?= .
EXE_DIR ?= ./build

# The executable's file name is generated from the main source's name
MAIN_SRC = $(MAIN_DIR)/main.c
EXECUTABLE = $(patsubst $(MAIN_DIR)/%.c,$(EXE_DIR)/%$(TARGET_EXTENSION),$(MAIN_SRC))

# Complete list of all source files to be compiled/linked for the build
SRC_FILES = $(wildcard ./foo/*.c ./bar/*.c ./*.c)

# Include dirs are assumed to be where the srcs are
INC_DIRS = $(dir $(SRC_FILES))
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

# List of all headers so we can track their existence as dependencies
INC_FILES=\
  $(wildcard $(INC_DIRS)/%.h)

# Special #defines desired for the build
SYMBOLS=

# Run the executable
default: clean $(EXE_DIR) $(EXECUTABLE)
	@-./$(EXECUTABLE)

# Compile/Link the executable from the sourcs and headers
$(EXECUTABLE): $(SRC_FILES) $(INC_FILES)
	@$(C_COMPILER) $(CFLAGS) $(INC_FLAGS) $(SYMBOLS) $(sort $(SRC_FILES)) -o $(EXECUTABLE)

# Make directory that holds generated files
$(EXE_DIR):
	@$(MKDIR) $@

# Delete old executable to force full compilation of sources
clean:
	@$(CLEANUP) $(EXE_DIR)/*$(TARGET_EXTENSION)
