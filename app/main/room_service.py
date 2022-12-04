"""
Problem Domain: Room Service represents all the hotel room service related operations
"""

from app.main.models import *

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

    
