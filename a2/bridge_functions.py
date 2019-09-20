""" 
Assignment 2: Bridges

The data used for this assignment is a subset of the data found in:
https://www.ontario.ca/data/bridge-conditions
"""

import csv
import math
from typing import List, TextIO

ID_INDEX = 0
NAME_INDEX = 1
HIGHWAY_INDEX = 2
LAT_INDEX = 3
LON_INDEX = 4
YEAR_INDEX = 5
LAST_MAJOR_INDEX = 6
LAST_MINOR_INDEX = 7
NUM_SPANS_INDEX = 8
SPAN_LENGTH_INDEX = 9
LENGTH_INDEX = 10
LAST_INSPECTED_INDEX = 11
BCIS_INDEX = 12

HIGH_PRIORITY_BCI = 60   
MEDIUM_PRIORITY_BCI = 70
LOW_PRIORITY_BCI = 100

HIGH_PRIORITY_RADIUS = 500  
MEDIUM_PRIORITY_RADIUS = 250
LOW_PRIORITY_RADIUS = 100

EARTH_RADIUS = 6371

####### BEGIN HELPER FUNCTIONS ####################

def read_data(csv_file: TextIO) -> List[List[str]]:
    """Read and return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of csv_file.

    Docstring examples not given since results depend on csv_file.
    """ 

    lines = csv.reader(csv_file)
    data = list(lines)[2:]
    return data


def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by   
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.
    
    >>> calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> calculate_distance(43.42, -79.24, 53.32, -113.30)
    2713.226
    """

    # This function uses the haversine function to find the
    # distance between two locations. You do NOT need to understand why it
    # works. You will just need to call on the function and work with what it
    # returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1), 
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1 
    lat_diff = lat2 - lat1 
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    return round(c * EARTH_RADIUS, 3)


def format_span(unformatted_data: str, span_count: int) -> List[float]:
    """Return a list of lengths of span_count spans of a bridge.
    
    >>> format_span('Total=64 (1)=12;(2)=19;(3)=21;(4)=12', 4)
    [12.0, 19.0, 21.0, 12.0]
    """
    
    formatted_spans = []
    first_equals = unformatted_data.find('=') + 1
    first_semicolon = 0
    for ch in range(span_count):
        start_point = unformatted_data.find('=', first_equals) + 1
        end_point = unformatted_data.find(';', first_semicolon)
        first_equals = start_point + 1
        first_semicolon = end_point + 1
        formatted_spans.append(float(unformatted_data[start_point:end_point]))
    return formatted_spans


def format_bci(bridge_data: List[list]) -> List[float]:
    """Return a formatted list of BCIs.
    
    >>> format_bci(['1 - 32/', 'Highway 24 Underpass at Highway 403', '403', \
    '43.167233', '-80.275567', '1965', '2014', '2009', '4', \
    'Total=64 (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '', \
    '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9', \
    ''])
    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]
    """
    
    formatted_bcis = []
    for bci in range(13, len(bridge_data)):
        if len(bridge_data[bci]) > 0 and bridge_data[bci]:
            formatted_bcis.append(float(bridge_data[bci]))
    return formatted_bcis


def get_bridges_within_high_radius(high_priority_bridges: List[List[str]], \
                                   inspector: List[float]) -> List[int]:
    """Return list of ids of bridges from high_priority_bridges within high \
    priority radius of inspector.
    
    >>> get_bridges_within_high_radius([], [66.32, -91.45])
    []
    """
    
    high_bridges_in_high_rad = []
    for bridge in high_priority_bridges:
        distances = find_bridges_in_radius(high_priority_bridges, inspector[0],\
                                           inspector[1], \
                                           HIGH_PRIORITY_RADIUS)
        if bridge[ID_INDEX] in distances:
            high_bridges_in_high_rad.append(bridge[ID_INDEX])
    return high_bridges_in_high_rad


def get_bridges_within_med_radius(med_priority_bridges: List[List[str]], \
                                   inspector: List[float]) -> List[int]:
    """Return list of ids of bridges from med_priority_bridges within med \
    priority radius of inspector.
    
    >>> get_bridges_within_medium_radius([], [66.32, -91.45])
    []
    """
    
    med_bridges_in_med_rad = []
    for bridge in med_priority_bridges:
        distances = find_bridges_in_radius(med_priority_bridges, inspector[0], \
                                           inspector[1], \
                                           MEDIUM_PRIORITY_RADIUS)
        if bridge[ID_INDEX] in distances:
            med_bridges_in_med_rad.append(bridge[ID_INDEX])
    return med_bridges_in_med_rad


def get_bridges_within_low_radius(low_priority_bridges: List[List[str]], \
                                   inspector: List[float]) -> List[int]:
    """Return list of ids of bridges from low_priority_bridges within low \
    priority radius of inspector.
    
    >>> get_bridges_within_low_radius([], [66.32, -91.45])
    []
    """
    
    low_bridges_in_low_rad = []
    for bridge in low_priority_bridges:
        distances = find_bridges_in_radius(low_priority_bridges, inspector[0], \
                                           inspector[1], HIGH_PRIORITY_RADIUS)
        if bridge[ID_INDEX] in distances:
            low_bridges_in_low_rad.append(bridge[ID_INDEX])
    return low_bridges_in_low_rad
    

####### END HELPER FUNCTIONS ####################

### SAMPLE DATA TO USE IN DOCSTRING EXAMPLES ####

THREE_BRIDGES_UNCLEANED = [
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

THREE_BRIDGES = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,
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

#################################################
def format_data(data: List[List[str]]) -> None:  
    """Modify data so that it follows the format outlined in the 
    'Data formatting' section of the assignment handout.
    
    >>> d = THREE_BRIDGES_UNCLEANED
    >>> format_data(d)
    >>> d == THREE_BRIDGES
    True
    """

    assignment_id = 1
    for info in data:
        # Run through each element of data and modifying it one-by-one to be
        # in proper formatted form
        info[ID_INDEX] = assignment_id
        assignment_id += 1
        info[HIGHWAY_INDEX] = str(info[HIGHWAY_INDEX])
        info[LAT_INDEX] = float(info[LAT_INDEX])
        info[LON_INDEX] = float(info[LON_INDEX])
        info[YEAR_INDEX] = str(info[YEAR_INDEX])
        info[LAST_MAJOR_INDEX] = str(info[LAST_MAJOR_INDEX])
        info[LAST_MINOR_INDEX] = str(info[LAST_MINOR_INDEX])
        info[NUM_SPANS_INDEX] = int(info[NUM_SPANS_INDEX])
        info[SPAN_LENGTH_INDEX] = format_span(info[SPAN_LENGTH_INDEX], \
                                              info[NUM_SPANS_INDEX])
        if len(info[LENGTH_INDEX]) > 0:
            info[LENGTH_INDEX] = float(info[LENGTH_INDEX])
        else:
            # Bridge Length becomes 0.0 if not assigned
            info[LENGTH_INDEX] = 0.0
        info[LAST_INSPECTED_INDEX] = str(info[LAST_INSPECTED_INDEX])
        info[BCIS_INDEX] = format_bci(info)
        # Removes any extra data provided to ensure data is in 
        # the proper formatted 13-element form
        while len(info) > 13:
            info.pop()


def get_bridge(bridge_data: List[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridge_data. If
    there is no bridge with the given id, return an empty list.  
    
    >>> result = get_bridge(THREE_BRIDGES, 1)
    >>> result == [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, \
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    """

    if bridge_id > len(bridge_data) or bridge_id < 0:
        return []
    return bridge_data[bridge_id - 1]


def get_average_bci(bridge_data: List[list], bridge_id: int) -> float:
    """Return the average BCI for the bridge with bridge_id from bridge_data.
    If there is no bridge with the id bridge_id, return 0.0. If there are no
    BCIs for the bridge with id bridge_id, return 0.0.
    
    >>> get_average_bci(THREE_BRIDGES, 1)
    70.88571428571429
    """
    
    average_BCI = 0.0
    bridge = get_bridge(bridge_data, bridge_id)
    if len(bridge) > 0 and len(bridge[BCIS_INDEX]) > 0:
        for bci in bridge[BCIS_INDEX]:
            average_BCI += bci
        average_BCI /= len(bridge[BCIS_INDEX])
        return average_BCI
    return 0.0    


def get_total_length_on_highway(bridge_data: List[list], highway: str) -> float:
    """Return the total length of bridges in bridge_data on highway.
    Use zero for the length of bridges that do not have a length provided.
    If there are no bridges on highway, return 0.0.
    
    >>> get_total_length_on_highway(THREE_BRIDGES, '403')
    126.0
    >>> get_total_length_on_highway(THREE_BRIDGES, '401')
    0.0
    """
    
    bridges_on_highway = []
    total_length = 0.0
    for bridge in bridge_data:
        if highway == bridge[HIGHWAY_INDEX]:
            bridges_on_highway.append(bridge)
    for bridge in bridges_on_highway:
        total_length += bridge[LENGTH_INDEX]
    return total_length


def get_distance_between(bridge1: list, bridge2: list) -> float:
    """Return the distance in kilometres, rounded to the nearest metre
    (i.e., 3 decimal places), between the two bridges bridge1 and bridge2.
        
    >>> get_distance_between(get_bridge(THREE_BRIDGES, 1), \
                                 get_bridge(THREE_BRIDGES, 2))
    1.968
    """

    return calculate_distance(bridge1[LAT_INDEX], bridge1[LON_INDEX], \
                       bridge2[LAT_INDEX], bridge2[LON_INDEX])
    
    
def find_closest_bridge(bridge_data: List[list], bridge_id: int) -> int:
    """Return the id of the bridge in bridge_data that has the shortest
    distance to the bridge with id bridge_id.
    
    Precondition: a bridge with bridge_id is in bridge_data, and there are
    at least two bridges in bridge_data
    
    >>> find_closest_bridge(THREE_BRIDGES, 2)
    1
    """

    distances = []
    new_bridges = bridge_data[:]
    bridge = get_bridge(bridge_data, bridge_id)
    new_bridges.remove(bridge)
    for bridges in new_bridges:
        distances.append(get_distance_between(bridge, bridges))
    return new_bridges[distances.index(min(distances))][ID_INDEX]


def find_bridges_in_radius(bridge_data: List[list], lat: float, long: float,
                           distance: float) -> List[int]:
    """Return the IDs of the bridges that are within radius distance
    from (lat, long).
    
    >>> find_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    [1, 2]
    """

    bridges_within_radius = []
    for bridge in bridge_data:
        if calculate_distance(bridge[LAT_INDEX], bridge[LON_INDEX], lat, long) \
                              <= distance:
            bridges_within_radius.append(bridge[ID_INDEX])
    return bridges_within_radius


def get_bridges_with_bci_below(bridge_data: List[list], bridge_ids: List[int],
                               bci_limit: float) -> List[int]:
    """Return the IDs of the bridges with ids in bridge_ids whose most
    recent BCIs are less than or equal to bci_limit.
    
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1, 2], 72)
    [2]
    """

    bridges_below_limit = []
    for id in bridge_ids:
        if len(bridge_data[id - 1][BCIS_INDEX]) > 0 and bridge_data[id - 1] \
           [BCIS_INDEX][0] <= bci_limit:
            bridges_below_limit.append(id)
    return bridges_below_limit


def get_bridges_containing(bridge_data: List[list], search: str) -> List[int]:
    """
    Return a list of IDs of bridges whose names contain search (case
    insensitive).
    
    >>> get_bridges_containing(THREE_BRIDGES, 'underpass')
    [1, 2]
    >>> get_bridges_containing(THREE_BRIDGES, 'Highway')
    [1]
    """

    bridges_with_search = []
    for bridge in bridge_data:
        if search.lower() in bridge[NAME_INDEX].lower():
            bridges_with_search.append(bridge[ID_INDEX])
    return bridges_with_search


def assign_inspectors(bridge_data: List[list], inspectors: List[List[float]],
                      max_bridges: int) -> List[List[int]]:
    """Return a list of bridge IDs to be assigned to each inspector in
    inspectors. inspectors is a list containing (latitude, longitude) pairs
    representing each inspector's location.
    
    At most max_bridges bridges should be assigned to an inspector, and each
    bridge should only be assigned once (to the first inspector that can
    inspect that bridge).
    
    See the "Assigning Inspectors" section of the handout for more details.
    
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 1)
    [[1]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 2)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 3)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 1)
    [[1], [2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 2)
    [[1, 2], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [45.0368, -81.34]], 2)
    [[1, 2], [3]]
    >>> assign_inspectors(THREE_BRIDGES, [[38.691, -80.85], [43.20, -80.35]], 2)
    [[], [1, 2]]
    """
            
    high_bridges = []
    medium_bridges = []
    low_bridges = []
    bridges_for_inspector = []
    # Accumulate bridges according to their priority, in lists
    for bridge in bridge_data:
        if bridge[BCIS_INDEX][0] <= HIGH_PRIORITY_BCI:
            high_bridges.append(bridge)
        elif bridge[BCIS_INDEX][0] <= MEDIUM_PRIORITY_BCI:
            medium_bridges.append(bridge)
        else:
            low_bridges.append(bridge)
    for inspector in inspectors:
        bridge = []
        while len(bridge) < max_bridges:
            # Assign high, medium, and low priority bridges to inspectors
            high_priority_in_rad = get_bridges_within_high_radius(high_bridges, \
                                                                  inspector)
            med_priority_in_rad = get_bridges_within_med_radius(medium_bridges, \
                                                                   inspector)
            low_priority_in_rad = get_bridges_within_low_radius(low_bridges, \
                                                                 inspector)
            # Assign bridges to inspectors from high to low priority
            # Remove bridges that are already assigned
            if len(high_priority_in_rad) > 0:
                bridge.append(high_priority_in_rad[0])
                high_priority_in_rad.remove(high_priority_in_rad[0])
                high_bridges.remove(high_bridges[0])
            elif len(med_priority_in_rad) > 0:
                bridge.append(med_priority_in_rad[0])
                med_priority_in_rad.remove(med_priority_in_rad[0])
                medium_bridges.remove(medium_bridges[0])
            elif len(low_priority_in_rad) > 0:
                bridge.append(low_priority_in_rad[0])
                low_priority_in_rad.remove(low_priority_in_rad[0])
                low_bridges.remove(low_bridges[0])
            else:
                break
        bridges_for_inspector.append(bridge)
    return bridges_for_inspector
                

def inspect_bridges(bridge_data: List[list], bridge_ids: List[int], date: str, 
                    bci: float) -> None:
    """Update the bridges in bridge_data with id in bridge_ids with the new
    date and BCI score for a new inspection.
    
    >>> bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,\
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, \
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,\
                                 73.3]], \
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', \
                  '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                 ]
    >>> inspect_bridges(bridges, [1], '09/15/2018', 71.9)
    >>> bridges == [[1, 'Highway 24 Underpass at Highway 403', '403', \
                     43.167233, -80.275567, '1965', '2014', '2009', 4, \
                     [12.0, 19.0, 21.0, 12.0], 65, '09/15/2018', \
                     [71.9, 72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], \
                     61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, \
                                          70.3, 73.3]], \
                    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, \
                     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                   ]
    True
    """

    for bridge in bridge_data:
        if bridge[ID_INDEX] in bridge_ids:
            bridge[LAST_INSPECTED_INDEX] = date
            bridge[BCIS_INDEX].insert(0, bci)


def add_rehab(bridge_data: List[list], bridge_id: int, new_date: str, 
              is_major: bool) -> None:
    """
    Update the bridge with the id bridge_id to have its last rehab set to
    new_date. If is_major is True, update the major rehab date. Otherwise,
    update the minor rehab date.
    
    >>> bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,\
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, \
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,\
                                 73.3]], \
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', \
                  '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                 ]
    >>> add_rehab(bridges, 1, '2018', False)
    >>> bridges == [[1, 'Highway 24 Underpass at Highway 403', '403', \
                     43.167233, -80.275567, '1965', '2014', '2018', 4, \
                     [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], \
                     61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, \
                                          70.3, 73.3]], \
                    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, \
                     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                   ]
    True
    """

    if is_major:
        bridge_data[bridge_id - 1][LAST_MAJOR_INDEX] = new_date
    else:
        bridge_data[bridge_id - 1][LAST_MINOR_INDEX] = new_date


if __name__ == '__main__':
    pass 

    # # To test your code with larger lists, you can uncomment the code below to
    # # read data from the provided CSV file.
    # bridges = read_data(open('bridge_data.csv'))
    # format_data(bridges)

    # # For example,
    # print(get_bridge(bridges, 3))
    # expected = [3, 'NORTH PARK STEET UNDERPASS', '403', 43.165918, -80.263791,
    #             '1962', '2013', '2009', 4, [12.2, 18.0, 18.0, 12.2], 60.8,
    #             '04/13/2012', [71.4, 69.9, 67.7, 68.9, 69.1, 69.9, 72.8]]
    # print('Testing get_bridge: ', \
    #      get_bridge(bridges, 3) == expected)
    