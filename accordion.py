import random

def accordion_function():
    room_4118 = False
    room_4119 = False
    room_4120 = False
    room_4121 = False
    room_4122 = False

    roomnumber_list = [room_4118, room_4119, room_4120, room_4121, room_4122] # an array with the bools above

    for i in range(len(roomnumber_list)):
        roomnumber_list[i] = bool(random.getrandbits(1)) # randomly assign True or False to each room
    print(roomnumber_list)
    return roomnumber_list
accordion_function()

def weekend_function():
    MONDAY          = 1
    TUESDAY         = 1
    WEDNSDAY        = 1
    THURSDAY        = 1
    FRIDAY          = 1

    daydate_list = [MONDAY, TUESDAY, WEDNSDAY, THURSDAY, FRIDAY] # an array with the ints above

    for a in range(len(daydate_list)):
        daydate_list[a] = int(random.getrandbits(3)) # randomly assign 3-bit number to each day
    print(daydate_list)
    return daydate_list
weekend_function()

def shuffled_function(element):
    roomnumber_list = accordion_function()
    daydate_list = weekend_function()
    combined_array = list(zip(roomnumber_list, daydate_list))
    random.shuffle(combined_array)
    mixedarray_list = [value for _, value in combined_array]
    print(mixedarray_list)
    return mixedarray_list
shuffled_function()



###

# Original arrays
data_array = [10, 20, 30, 40, 50]
reference_array = [1, 2, 3, 4, 5]

# Function to get a randomized version of the data array for a given element in the reference array
def get_randomized_array(element):
    combined_array = list(zip(reference_array, data_array))
    random.shuffle(combined_array)
    shuffled_data_array = [value for _, value in combined_array]
    return shuffled_data_array

# Example usage
index_to_randomize = 2
result = get_randomized_array(index_to_randomize)