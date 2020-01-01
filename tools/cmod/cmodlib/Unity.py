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

class TestResult():
    def __init__( self, source_file=None, line=None, test_group=None, test_case=None, result=None, message=None ):
        self.source_file = source_file
        self.line = line
        self.test_group = test_group
        self.test_case = test_case
        self.result = result
        self.message = message

    def __str__(self):
        return self.format_test_output_terminal()

    def format_test_output_terminal( self ):
        if self.result == "FAIL":
            output = "   \033[91m " + self.result + ":\033[00m   " + os.path.basename(self.source_file) + ":" + self.line + " - " + self.test_case
        elif self.result == "IGNORE":
            output = "   \033[93m " + self.result + ":\033[00m " + os.path.basename(self.source_file) + ":" + self.line + " - " + self.test_case
        elif self.result == "PASS":
            output = "   \033[92m " + self.result + ":\033[00m   " + self.test_case
        if self.message:
            output += ": " + self.message
        # print(output)
        return output

    def format_results_file( self ):
        output = "    " + self.result + ": " + os.path.basename(self.source_file) + ":" + self.line + " - " + self.test_case
        if self.message:
            output += ": " + self.message
        return output

class TestSummary():
    def __init__(self, total=0, passed=0, failed=0, ignored=0):
        self.total = total
        self.passed = passed
        self.failed = failed
        self.ignored = ignored

class UnityOutput():
    def __init__(self, path):
        self.test_output_filepath = os.path.normpath( path )
        self.result_list = None
        self.summary = None

    def read_test_output( self ):
        # print("Reading", self.test_output_filepath)
        lineList = list()
        result_list = list()

        if os.path.isfile( self.test_output_filepath ):
            with open(self.test_output_filepath, 'r') as fi:
                for line in fi:
                    lineList.append(line.rstrip('\n'))
                # This just prints the entire file
                for line in lineList:
                    # print(line)
                    # This regex matches most everything at the front-end, but combines the FAIL:result and the possible message
                    # To be searched for later. Its ok to not have a message!
                    results_match = re.search( r'\.*([a-zA-Z].*):([\d]+).*:TEST\s*\(\s*(.*),\W*(.*)\s*\)\s*:\s*(.*)\s*:?', line )

                    # Get the Unity test summary
                    test_summary = re.search( r'(\d+) Tests (\d+) Failures (.+) Ignored', line )

                    if results_match:
                        status_match = re.search( r'^([A-Z]*):?', results_match.group(5) )
                        message_match = re.search( r'^.*:\s*(.+)$', results_match.group(5) )

                        # Not every test case has a message
                        if message_match:
                            message = message_match.group(1)
                        else:
                            message = ''

                        result_list.append( TestResult( results_match.group(1), \
                                                        results_match.group(2), \
                                                        results_match.group(3), \
                                                        results_match.group(4), \
                                                        status_match.group(1), \
                                                        message \
                                                        ) \
                                            )
                    if test_summary:
                        summary = [ test_summary.group(1), test_summary.group(2), test_summary.group(3) ]
                        totals = TestSummary( total = int(summary[0]), \
                            passed = int(summary[0]) - ( int(summary[1]) + int(summary[2]) ), \
                                failed = int(summary[1]), \
                                    ignored = int(summary[2]) )
                # [print( result ) for result in result_list]
                fi.close()
        else:
            result_list.append( TestResult() )
            totals = TestSummary(0,0,0,0)

        return result_list, totals
