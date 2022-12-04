"""
Problem Domain: it holds all the models that represent the hotel room assignment problem primary entities
"""
from enum import Enum

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
  def __init__(self, no_of_flloors = 4, rooms_on_floor = 5) -> None:
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

  def _fetch_only_available(self):
    """
    :purpose: it only fetch those rooms whose status is currently available
    """
    self.__available_rooms = filter(lambda room: room.status == RoomStatus.AVAILABLE, self.__hotel_rooms)


  def _fetch_room_index(self, input_room: Room):
    """
    :purpose: return the room index based on room number of the given room
    """
    floor_no = input_room.room_number[0]
    suffix = input_room.room_number[1]

    indx_first_room = (floor_no - 1) * self.__rooms_on_floor

    return indx_first_room + (ord(suffix) - ord('A'))

  def assign_room(self) -> str:
    """
    :purpose: it assigns the nearest available and returns that room number
    """
    avl_room = None

    if self.__available_rooms:
        avl_room = self.__available_rooms[0]

        # mark the room as allocated
        indx_avl_room = self._fetch_room_index(avl_room) 

        self.__hotel_rooms[indx_avl_room].room_status = RoomStatus.OCCUPIED

        self.__available_rooms.remove(avl_room)

    return avl_room.room_number if avl_room else avl_room


  def check_out_room(self, room_to_checkout: Room) -> bool:
    """
    :purpose: change room status as "vaccant" on check out room
    """
    indx_room = self._fetch_room_index(room_to_checkout)

    if indx_room:
      self.__hotel_rooms[indx_room].room_status = RoomStatus.VACCANT
    
    # TODO handle user exceptions
    return True



  def clean_room(self, room_to_clean: Room) -> bool:
    room_indx = self._fetch_room_index(room_to_clean)

    self.__hotel_rooms[room_indx].room_status = RoomStatus.AVAILABLE
    
    # update the available room list
    self._fetch_only_available()

  def repair_room(self, room_to_repair: Room) -> bool:
    room_indx = self._fetch_room_index(room_to_repair)

    self.__hotel_rooms[room_indx].room_status = RoomStatus.REPAIR

    # TODO handle validation
    return True

  def list_all_available_rooms(self) -> list:
    return self.__available_rooms


