"""
Problem Domain: it holds all the models that represent the hotel room assignment problem primary entities
"""
from enum import Enum
from app.main.exceptions import *

class RoomStatus(str, Enum):
    """
    : purpose: it represents the room status passwhich is one f
      > available
      > occupied
      > vacant
      > repair
    """
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    VACCANT = "VACCANT"
    REPAIR = "REPAIR"

class Room:
    """
    :purpose: Room represents the hotel room which will be assigned to guests
    Every room has
    - a room number: floor number prefix followed by a single alphabet(suffix)
      e.g 1A, 1B, 1C etc
    - status : represents room status 
    """
    def __init__(self, room_number, room_status=RoomStatus.AVAILABLE) -> None:
        self.__room_number = room_number
        self.__room_status = room_status
    
    @property
    def room_number(self):
        return self.__room_number
    
    @room_number.setter
    def room_number(self, room_number: int):
      self.__room_number = room_number
    
    @property
    def room_status(self):
      return self.__room_status
    
    @room_status.setter
    def room_status(self, room_status: RoomStatus):
      self.__room_status = room_status


class Hotel:
  """
  :purpose: Hotel has separate Room and represents the main Hotel 
  in the Hotel service app and has different floors consisting of 
  - Room :  room which will be allocated to guests

  Note:
  The route to each room from entrance is defined in zig-zag order
  and odd floor room with A series being nearest to entrance
  while on even floor room with E series being nearest to entrance 
  """
  def __init__(self, no_of_flloors,rooms_on_floor) -> None:
    self.__no_of_floors = no_of_flloors
    self.__rooms_on_floor = rooms_on_floor
    self.__hotel_rooms = []
    self.__available_rooms = []

    a_ascii = 65

    # intialize the Hotel with all rooms initially 
    for floor in range(1, no_of_flloors + 1):
      for room in range(1, rooms_on_floor + 1):

        if floor % 2 == 0:
          room_number = str(floor) + chr(a_ascii + (rooms_on_floor - room))
        else:
          room_number = str(floor) + chr(a_ascii + room - 1)

        self.__hotel_rooms.append(Room(room_number)) 

    # initialize the available rooms list
    self._fetch_only_available() 
  
  @property
  def no_of_floors(self) -> int:
    return self.__no_of_floors
  
  @no_of_floors.setter
  def no_of_floors(self, no_of_floors):
    self.__no_of_floors = no_of_floors

  @property
  def rooms_on_floor(self) -> int:
    return self.__rooms_on_floor
  
  @rooms_on_floor.setter
  def rooms_on_floor(self, rooms_on_floor):
    self.__rooms_on_floor = rooms_on_floor

  @property
  def total_rooms(self):
    return self.no_of_floors * self.rooms_on_floor

  def get_all_hotel_rooms(self):
    return self.__hotel_rooms
    
  def _fetch_only_available(self):
    """
    :purpose: it only fetch those rooms whose status is currently available
    """
    self.__available_rooms = list(filter(lambda room: room.room_status == RoomStatus.AVAILABLE, self.__hotel_rooms))


  def _fetch_room_index(self, input_room_number: str):
    """
    :purpose: return the room index based on room number of the given room
    """
    floor_no = int(input_room_number[0])
    suffix = input_room_number[1]

    if floor_no == '-':
      return -1

    indx_first_room = (floor_no - 1) * self.__rooms_on_floor

    return indx_first_room + (ord(suffix) - ord('A'))

  def get_room(self, room_number: str) -> Room:
    """
    :purpose: for the given room_number fetches and returns the room object if found
    else raises RoomNotFound exception if invalid room_number is provided
    """
    room_indx = self._fetch_room_index(room_number)

    if room_indx >= 0 and room_indx <= self.total_rooms:
      return self.__hotel_rooms[room_indx]
    else:
      raise RoomNotFound()

  def assign_room(self) -> str:
    """
    :purpose: it assigns the nearest available and returns that room number
    """
    avl_room = None

    if self.__available_rooms:
        avl_room = self.__available_rooms[0]

        # mark the room as allocated
        indx_avl_room = self._fetch_room_index(avl_room.room_number) 

        self.__hotel_rooms[indx_avl_room].room_status = RoomStatus.OCCUPIED

        self.__available_rooms.remove(avl_room)

    return avl_room.room_number if avl_room else avl_room


  def check_out_room(self, room_to_checkout: Room) -> bool:
    """
    :purpose: change room status as "vaccant" on check out room
    """
    if room_to_checkout.room_status != RoomStatus.OCCUPIED:
      raise InvalidRoomOperation()

    room_indx = self._fetch_room_index(room_to_checkout.room_number)

    self.__hotel_rooms[room_indx].room_status = RoomStatus.VACCANT
    

  def clean_room(self, room_to_clean: Room) -> bool:

    if room_to_clean.room_status != RoomStatus.VACCANT:
      if room_to_clean.room_status == RoomStatus.AVAILABLE:
        raise RoomWillBeUsed()
      else:
        raise RoomInUse()
    
    room_indx = self._fetch_room_index(room_to_clean.room_number)

    self.__hotel_rooms[room_indx].room_status = RoomStatus.AVAILABLE
    
    # update the available room list
    self._fetch_only_available()


  def repair_room(self, room_to_repair: Room) -> bool:
    if room_to_repair.room_status != RoomStatus.VACCANT:
      if room_to_repair.room_status == RoomStatus.AVAILABLE:
        raise RoomWillBeUsed()
      else:
        raise RoomInUse()

    room_indx = self._fetch_room_index(room_to_repair.room_number)

    self.__hotel_rooms[room_indx].room_status = RoomStatus.REPAIR


  def list_all_available_rooms(self) -> list:
    return self.__available_rooms


