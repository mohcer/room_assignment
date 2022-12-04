"""
Problem Domain: Room Service represents all the hotel room service related operations
"""
import logging 
import traceback

from app.main.models import *
from app.main.exceptions import *

class HotelService():
    """
    HotelService helps a bootique hotel to carryout its operation as follows 
    - assigns a nearest available room to guest, room becomes occupied
    - checkout a guest, room becomes vacant
    - clean a room, room becomes available 
    - repair a room, room become under repair
    
    These operation can only be carried out in below manner that transitions the room status only that order
    available --check-in--> occupied
    occupied --check-out--> vacant
    vacant --clean--> available
    vacant --out-of-service--> repair
    repair --repaired--> vaccant     
    """
    def __init__(self, no_of_floors = 4, rooms_on_floor = 5) -> None:
        self.__hotel = Hotel(no_of_floors, rooms_on_floor)

    def _validate_room_number(self, room_number):

        if len(room_number) != 2:
            status = False
        else:
            floor_no = int(room_number[0])
            suffix = room_number[1]

            last_room_on_floor = ord('A') + self.__hotel.rooms_on_floor
            if floor_no in range(1, self.__hotel.no_of_floors + 1) and ord(suffix) in range(ord('A'), last_room_on_floor):
                status = True
            else:
                status = False
        
        if not status:
            raise RoomNotFound()

    def assign_room(self):
        return self.__hotel.assign_room()

    def check_out_room(self, room_number: str):
        try:
            # validate room number
            self._validate_room_number(room_number)
            
            # if valid room_number fetch the room details
            room_to_checkout = self.__hotel.get_room(room_number)

            # checkout room
            self.__hotel.check_out_room(room_to_checkout)
        except RoomNotFound as e:
            print(e)
        except RoomWillBeUsed as e:
            print(e)
        except InvalidRoomOperation as e:
            print(e)
        else:
            print(f"Guest checked out successfully from room : {room_number}")

    def clean_room(self, room_number: str):
        try:
            # validate room number
            self._validate_room_number(room_number)

            # if valid room_number fetch the room details
            room_to_clean = self.__hotel.get_room(room_number)

            # clean room
            self.__hotel.clean_room(room_to_clean)
        except RoomNotFound as e:
            print(e)
        except RoomWillBeUsed as e:
            print(e)
        except InvalidRoomOperation as e:
            print(e)
        else:
            print(f"Room {room_number} cleaned successfully!")

    def repair_room(self, room_number):
        try:
            # validate room number
            self._validate_room_number(room_number)

            # if valid room_number fetch the room details
            room_to_repair = self.__hotel.get_room(room_number)

            # repair room
            self.__hotel.repair_room(room_to_repair)
        except RoomNotFound as e:
            print(e)
        except RoomWillBeUsed as e:
            print(e)
        except InvalidRoomOperation as e:
            print(e)
        else:
            print(f"Room {room_number} cleaned successfully!")

    def get_all_list_of_available_rooms(self):
        avl_rooms = self.__hotel.list_all_available_rooms()

        if avl_rooms:
            print("The following rooms are available:")
            for room in avl_rooms:
                print(f"Room - {room.room_number} is available")
        else:
            print("Sorry! No room is available at the moment!")

if __name__ == '__main__':
    hotel_service = HotelService()

    print("Hotel Service Initialized .............")
    print("You can perform the following operations by selecting the correct option from the below menu")
    
    while True:
        print("1) assign room")
        print("2) checkout room")
        print("3) clean room")
        print("4) repair room")
        print("5) list all available rooms")
        print("6) exit")

        try:
            choice = int(input("Enter your choice "))

            if choice == 1:
                print("You choose to assign room")

                room_number_alloted = hotel_service.assign_room()

                if room_number_alloted:
                    print(f"Room alloted to guest : {room_number_alloted}")
                else:
                    print(f"Sorry no room is available!. Please wait for other guests to checkout ")
            elif choice == 2: 
                print("You choose to checkout room")

                room_number = input("Please enter the room number of the guest to checkout! ")
                hotel_service.check_out_room(room_number)
            elif choice == 3:
                print("You choose to clean room")

                room_number = input("Please enter the room number to perform cleaning ")
                hotel_service.clean_room(room_number)
            elif choice == 4:
                print("You choose to repair room")

                room_number = input("Please enter the room number to perform repairing ")
                hotel_service.repair_room(room_number)
            elif choice == 5:
                print("You chooce to list all available rooms")

                hotel_service.get_all_list_of_available_rooms()

            elif choice == 6:
                print("You choose to exit")
                exit(0)
            else:
                print("Invalid choice.... Try again! \n")
        except ValueError as e:
            print("Invalid choice. Try again!")
        except Exception as e:
            print(e)
            print(traceback.format_exc())