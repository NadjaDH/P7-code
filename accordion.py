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

