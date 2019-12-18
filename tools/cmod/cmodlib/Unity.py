import os
import re
from collections import defaultdict

class UnitTest():
    def __init__(self, name=None, line=0 ):
        self.name = name
        self.line_number = line
        self.result = INIT

class TestGroup():
    def __init__(self, name=None, test_list=None):
        self.name = name
        self.testList = test_list

PASS = 0
SKIP = 1
FAIL = 2
INIT = 3

# Sources are not necessarily restricted to a single test groups,
# and groups to single sources, just use this class as a space to
# store collections of groups, and the group and test simlarities can be
# Reconciled during a sorting process to ensure the module ultimately owns
# the test group and tests
class TestSrc():
    def __init__(self, path):
        self.path = os.path.normpath( path )
        self.TestGroups = None # self.getTestGroups( self.path )

    def __str__(self):
        return str(self.path)

    # Finds all test groups and test cases, returning a list of test group objects
    def getTestGroups( self ):
        temp_group_list = list()
        temp_test_list = list()
        group_list = list()			# Start a list of the test groups we find in the tuple list
        test_list_of_lists = list() # Start a list of tests for each test group found in group_list

        test_group_pairs_regex = r'\n\w*TEST\(\s*([\S]+)\s*,\s*([\S]+)\s*\)'
        with open(self.path, "r") as f:
            matches = re.findall( test_group_pairs_regex, f.read() )	# Get list of tuples
            if matches:
                # print("matches =", matches, "\n")
                res = defaultdict(list)				# Create a blank dictionary
                for i, j in matches:				# Match group1 and group2 ( test group and test name respectively )
                    res[j].append(i)				# The test name is the key to this dictionary
                    temp_group_list.append( i )		# Remember the order in which things were added to the dictionary
                    temp_test_list.append( j )		# Make parallel lists of groups and tests

                for test_name in temp_test_list:	# For each test we found, in the order we found them,
                    if not res[test_name][0] in group_list:		# Add it's group to the group list if not there already
                        group_list.append(*res[test_name])		# Escape the weird list of a list thing going on here
                        test_list_of_lists.append(list())		# Append a new list to the test list list
                        test_list_of_lists[group_list.index(res[test_name][0])].append(test_name)	# Add the test name to it
                    else:
                        test_list_of_lists[group_list.index(res[test_name][0])].append(test_name)	# Add the test name to the appropriate list

                test_group_obj_list = list()
                for group in range(len(group_list)):
                    test_group_obj_list.append( TestGroup( group_list[group], test_list_of_lists[group] ) )
                    # print( test_group_obj_list[group] )
            f.close()
            # print("temp_test_list =", temp_test_list)
            # print("group list =", group_list)
            # print("lol =", test_list_of_lists)
            # print("\n")
        self.TestGroups = test_group_obj_list
        return test_group_obj_list
