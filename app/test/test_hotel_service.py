"""
Problem Domain: It represents all the unit test that ensures correct hotel operations
"""
import time
import unittest
from app.main.models import RoomStatus
from app.main.hotel_service import HotelService
from app.main.exceptions import *

class HotelServiceTesting(unittest.TestCase):
    hotel_service = HotelService()

    def test_init_hotel(self):
        # test default no of floors and no of rooms on each floor
        self.assertEqual(self.hotel_service.get_no_of_floors(), 4)
        self.assertEqual(self.hotel_service.get_rooms_on_floor(), 5)
    
    def test_assign_room(self):
        # test assign room nearest to the entrance
        self.assertEqual(self.hotel_service.assign_room(), "1A")
        self.assertEqual(self.hotel_service.assign_room(), "1B")

        room = self.hotel_service.get_hotel().get_room("1A")

        self.assertEqual(room.room_status, RoomStatus.OCCUPIED)

    def test_checkout_room(self):
        # assign room
        guest1_room = self.hotel_service.assign_room()
        guest2_room = self.hotel_service.assign_room()

        self.hotel_service.check_out_room(guest1_room)
        room1 = self.hotel_service.get_hotel().get_room(guest1_room)
        room2 = self.hotel_service.get_hotel().get_room(guest2_room)

        self.assertEqual(room1.room_status, RoomStatus.VACCANT)
        self.assertEqual(room2.room_status, RoomStatus.OCCUPIED)

    def test_clean_room(self):
        # assign room
        guest1_room = self.hotel_service.assign_room()

        self.hotel_service.check_out_room(guest1_room)
        
        # now clean the room
        self.hotel_service.clean_room(guest1_room)

        room1 = self.hotel_service.get_hotel().get_room(guest1_room)

        self.assertEqual(room1.room_status, RoomStatus.AVAILABLE)
    
    def test_repair_room(self):
        guest1_room = self.hotel_service.assign_room()

        self.hotel_service.check_out_room(guest1_room)

        # once the room becomes vaccant repair room
        self.hotel_service.repair_room(guest1_room)

        room1 = self.hotel_service.get_hotel().get_room(guest1_room)

        self.assertEqual(room1.room_status, RoomStatus.REPAIR)
    
    def test_invalid_room_operation(self):
        guest1_room = self.hotel_service.assign_room()

        self.hotel_service.check_out_room(guest1_room)

        # clean room 
        self.hotel_service.clean_room(guest1_room)
        
        room1 = self.hotel_service.get_hotel().get_room(guest1_room)
        
        self.assertEqual(room1.room_status, RoomStatus.AVAILABLE)
        
        # once a room is checked out and cleaned , again a checkout operation on that room would be invalid operation
        try:
            self.hotel_service.get_hotel().check_out_room(room1)
        except Exception as e:
            self.assertEqual(type(e), InvalidRoomOperation)

    def test_room_already_in_use(self):
        guest1_room = self.hotel_service.assign_room()

        # once room is still occupied calling a repair operation on that room would result in room in use
        room1 = self.hotel_service.get_hotel().get_room(guest1_room)

        try:
            self.hotel_service.get_hotel().repair_room(room1)
        except Exception as e:
            self.assertEqual(type(e), RoomInUse)
    
    def test_invalid_room_number(self):
        guest1_room = self.hotel_service.assign_room

        # inputing invalid room number will lead to Room not Found InvalidRoom
        try:
            room1 = self.hotel_service.get_hotel().get_room("1hk")
        except Exception as e:
            self.assertEqual(type(e), RoomNotFound)
        
        # inputing valid room number format but out of range room number along floor or suffix will also lead to Room not Found 
        try:
            room1 = self.hotel_service.get_hotel().get_room("1Q")
        except Exception as e:
            self.assertEqual(type(e), RoomNotFound)
        
        # room numbers are expected to be input as number prefix followed by charachter in upper case
        # inputing suffix as valid but lower case will also result in room not found 
        # e.g instead of 1A user types 1a
        try:
            room1 = self.hotel_service.get_hotel().get_room("1a")
        except Exception as e:
            self.assertEqual(type(e), RoomNotFound)
        
        # Valid case
        room1 = self.hotel_service.get_hotel().get_room("1A")

        self.assertEqual(room1.room_number, "1A")
    
    def test_list_all_available_rooms(self):
        all_rooms = self.hotel_service.get_hotel().list_all_available_rooms()

        # considering the above assign, checkout clean sequence there are 16 available rooms
        self.assertEqual(len(all_rooms), 16)

if __name__ == '__main__':
    unittest.main()