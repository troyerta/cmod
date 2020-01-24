MODULE_DIR = MODULE_A/module_a
PROJ_ROOT = ../../
# Missing unity dir - could be in config, or just derived in Makefile using $(PROJ_ROOT)
SRC_DIRS = . unit_testing/tests unit_testing/runners
HDR_DIRS = .   # also missing test harness
EXE_DIR = unit_testing/exe
RESULTS_DIR = unit_testing/results
RESULTS_TXT_PREFIX =
RESULTS_TXT_SUFFIX = _results

include $(PROJ_ROOT)/unit_test/module_makefile

config.ini changes:

Question: Can we just tell the Makefile to find/use the globs?

Yes, if we use the 'foreach' function:

SRC_DIRS = . ../../unit_testing/unity unit_test/tests unit_test/runners
REGEXS = .*c test_.*_tests.c test_.*_runner.c

SRC_FILES := $(foreach regex, $(REGEXS) $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/$(regex) ) )
SORTED = $(sort $(SRC_FILES))


# It might be prudent to simply list all the files in the module
# Makefile at this point, since it's getting rather complex.

Let cmod do all the file matching, searching and sorting, and simply
place the right list into the module Makefile once, then allow for
new sources and headers in the module by simply editing the Makefile.

Would that be too much? Enough?

If we can promise the user that the regex is followed, then we could
simply add a line like this for each file descriptor:

SRC_FILES = $(wildcard .*.c) \
SRC_FILES += $(wildcard ../../unit_testing/unity/.*c) \ # (Based on
    test harness config)
SRC_FILES += $(wildcard test/tests/test_*_tests.c)
SRC_FILES += $(wildcard test/tests/test_*_runners.c)

This should be good, repeated use of non-calculated information.
Make can do this sort of work for us, we just provide the directory
and the regex.

