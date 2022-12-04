class RoomNotFound(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Invalid Hotel Room!")


class RoomInUse(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Sorry! Room is in use please try again later.")

class RoomWillBeUsed(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Sorry cannot perform this operation, Room is already cleaned and ready to be assigned to guests!")

class InvalidRoomOperation(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Invalid Room operation!")