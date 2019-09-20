"""Checker for CSCA08 Assignment 2"""

import sys

sys.path.insert(0, './pyta')

print("================= Start: checking coding style =================")

import python_ta
python_ta.check_all('bridge_functions.py', config='pyta/a2_pyta.txt')

print("================= End: checking coding style =================\n")

print("================= Start: checking parameter and return types =================")

import builtins
import bridge_functions as bf # imported here so code that doesn't import correctly gets style checked


# Get the initial values of the constants
CONSTS_BEFORE = [bf.ID_INDEX, bf.NAME_INDEX, bf.HIGHWAY_INDEX, bf.LAT_INDEX,
                 bf.LON_INDEX, bf.YEAR_INDEX, bf.LAST_MAJOR_INDEX, 
                 bf.LAST_MINOR_INDEX, bf.NUM_SPANS_INDEX, bf.SPAN_LENGTH_INDEX,
                 bf.LENGTH_INDEX, bf.LAST_INSPECTED_INDEX, bf.BCIS_INDEX, 
                 bf.HIGH_PRIORITY_BCI, bf.MEDIUM_PRIORITY_BCI, bf.LOW_PRIORITY_BCI,
                 bf.HIGH_PRIORITY_RADIUS, bf.MEDIUM_PRIORITY_RADIUS,
                 bf.LOW_PRIORITY_RADIUS, bf.EARTH_RADIUS]

# Check for use of functions print and input.

our_print = print
our_input = input

def disable_print(*_args, **_kwargs):
    """ Notices if print is called """
    raise Exception("You must not call built-in function print!")


def disable_input(*_args, **_kwargs):
    """ Notices if input is called """
    raise Exception("You must not call built-in function input!")

builtins.print = disable_print
builtins.input = disable_input

# sample data for testing
sample_bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, 
                   -80.275567, '1965', '2014', '2009', 4, 
                   [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012', 
                   [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], 
                  [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, 
                   '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, 
                   '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,
                                  73.3]], 
                  [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958',
                   '2013', '', 1, [16.0], 18.4, '08/28/2013',
                   [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]
                 ]

# Type checks and simple checks for bridge_functions module

# Type and simple check bridge_functions.get_bridge
our_print('Checking get_bridge...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]

    
result = bf.get_bridge(sample, 1)
assert isinstance(result, list), \
    '''bridge_functions.get_bridge should return a list'''
assert len(result) == 13, \
    '''bridge_functions.get_bridge should return a list of length 13'''
assert isinstance(result[0], int), \
    '''the first value in the list returned by bridge_functions.get_bridge should be a int'''
assert isinstance(result[1], str), \
    '''the second value in the list returned by bridge_functions.get_bridge should be an str'''
assert isinstance(result[2], str), \
    '''the third value in the list returned by bridge_functions.get_bridge should be an str'''
assert isinstance(result[3], float), \
    '''the fourth value in the list returned by bridge_functions.get_bridge should be an float'''
assert isinstance(result[4], float), \
    '''the fifth value in the list returned by bridge_functions.get_bridge should be an float'''
assert isinstance(result[5], str), \
    '''the sixth value in the list returned by bridge_functions.get_bridge should be an str'''
assert isinstance(result[6], str), \
    '''the seventh value in the list returned by bridge_functions.get_bridge should be an str'''
assert isinstance(result[7], str), \
    '''the eighth value in the list returned by bridge_functions.get_bridge should be an str'''
assert isinstance(result[8], int), \
    '''the ninth value in the list returned by bridge_functions.get_bridge should be an int'''
assert isinstance(result[9], list), \
    '''the tenth value in the list returned by bridge_functions.get_bridge should be an list'''
assert isinstance(result[10], float), \
    '''the eleventh value in the list returned by bridge_functions.get_bridge should be a float'''
assert isinstance(result[11], str), \
    '''the twelfth value in the list returned by bridge_functions.get_bridge should be an str'''
assert isinstance(result[12], list), \
    '''the thirteenth value in the list returned by bridge_functions.get_bridge should be an list'''
our_print('  check complete')

# Type and simple check bridge_functions.get_average_bci
our_print('Checking get_average_bci...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.get_average_bci(sample, 1)
assert isinstance(result, float), \
    '''bridge_functions.get_average_bci should return a float'''
our_print('  check complete')

    
#Type and simple check for bridge_functions.get_total_length_on_highway
our_print('Checking get_total_length_on_highway...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.get_total_length_on_highway(sample, '403')
assert isinstance(result, float), \
    '''bridge_functions.get_total_length_on_highway should return a float'''
our_print('  check complete')
    
#Type and simple check for bridge_functions.get_distance_between
our_print('Checking get_distance_between...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.get_distance_between(sample[0], sample[1])
assert isinstance(result, float), \
    '''bridge_functions.get_distance_between should return a float'''
our_print('  check complete')


#Type and simple check bridge_functions.find_closest_bridge
our_print('Checking find_closest_bridge...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.find_closest_bridge(sample, 1)
assert isinstance(result, int), \
       '''bridge_functions.find_closest_bridge should return an int'''
our_print('  check complete')


#Type and simple check bridge_functions.find_bridges_in_radius
our_print('Checking find_bridges_in_radius...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.find_bridges_in_radius(sample, 43.0, -80.0, 1000)
assert isinstance(result, list), \
    '''bridge_functions.find_bridges_in_radius should return a list'''
for item in result:
    assert isinstance(item, int), \
           '''bridge_functions.find_bridges_in_radius should return a list of ints'''
our_print('  check complete')


#Type and simple check bridge_functions.get_bridges_with_bci_below
our_print('Checking get_bridges_with_bci_below...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.get_bridges_with_bci_below(sample, [1, 2, 3], 100)

assert isinstance(result, list), \
    '''bridge_functions.get_bridges_with_bci_below should return a list'''
for item in result:
    assert isinstance(item, int), \
           '''bridge_functions.get_bridges_with_bci_below should return a list of ints'''
our_print('  check complete')


#Type and simple check bridge_functions.assign_inspectors
our_print('Checking assign_inspectors...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.assign_inspectors(sample, [[43.164531, -80.251582]], 2)

assert isinstance(result, list), \
    '''bridge_functions.assign_inspectors should return a list'''
for item in result:
    assert isinstance(item, list), \
           '''bridge_functions.assign_inspectors should return a list of lists'''
    
    for id_ in item:
        assert isinstance(id_, int), \
               '''bridge_functions.assign_inspectors should return a list of lists of ints'''
our_print('  check complete')

      
#Type and simple check bridge_functions.get_bridges_containing
our_print('Checking get_bridges_containing...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.get_bridges_containing(sample, 'underpass')

assert isinstance(result, list), \
    '''bridge_functions.get_bridges_containing should return a list'''
for item in result:
    assert isinstance(item, int), \
           '''bridge_functions.get_bridges_containing should return a list of ints'''
our_print('  check complete')


#Type and simple check bridge_functions.format_data
our_print('Checking format_data...')
sample = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233', 
     '-80.275567', '1965', '2014', '2009', '4', 
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''], 
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582', 
     '1963', '2014', '2007', '4', 
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012', 
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''], 
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
    ]
result = bf.format_data(sample)
assert isinstance(result, type(None)), \
    '''bridge_functions.format_data should return None'''
our_print('  check complete')


#Type and simple check bridge_functions.inspect_bridges
our_print('Checking inspect_bridges...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.inspect_bridges(sample, [1, 2], "01/01/2001", 50)
assert isinstance(result, type(None)), \
    '''bridge_functions.inspect_bridges should return None'''
our_print('  check complete')


#Type and simple check bridge_functions.add_rehab
our_print('Checking add_rehab...')
sample = [inner[:] for inner in sample_bridges]
for lst in sample:
    lst[9] = lst[9][:]
    lst[12] = lst[12][:]
    
result = bf.add_rehab(sample, 2, "01/01/2001", True)
assert isinstance(result, type(None)), \
    '''bridge_functions.add_rehab should return None'''
our_print('  check complete')


builtins.print = our_print
builtins.input = our_input 

print("================= End: checking parameter and return types =================\n")

print('========== Start: checking whether constants are unchanged ==========')

# Get the final values of the constants
CONSTS_AFTER = [bf.ID_INDEX, bf.NAME_INDEX, bf.HIGHWAY_INDEX, bf.LAT_INDEX,
                bf.LON_INDEX, bf.YEAR_INDEX, bf.LAST_MAJOR_INDEX, 
                bf.LAST_MINOR_INDEX, bf.NUM_SPANS_INDEX, bf.SPAN_LENGTH_INDEX,
                bf.LENGTH_INDEX, bf.LAST_INSPECTED_INDEX, bf.BCIS_INDEX, 
                bf.HIGH_PRIORITY_BCI, bf.MEDIUM_PRIORITY_BCI, bf.LOW_PRIORITY_BCI,
                bf.HIGH_PRIORITY_RADIUS, bf.MEDIUM_PRIORITY_RADIUS,
                bf.LOW_PRIORITY_RADIUS, bf.EARTH_RADIUS]

# Check whether the constants are unchanged.
print('Checking constants...')
assert CONSTS_BEFORE == CONSTS_AFTER, \
       ('Your function(s) modified the value of some constant(s). Edit your' +
        '\ncode so that the values of constants are unchanged by your' +
        ' functions.')
print('  check complete')

print('=========== End: checking whether constants are unchanged ===========')


print("The parameter and return type checker passed.")
print("This means we will be able to test your code.")
print("It does NOT mean your code is necessarily correct.")
print("You should run your own thorough tests to convince yourself your code is correct.")
print()
print("Review the messages above to see the results of the style checking.")
