import random
from pydantic import BaseModel


class User(BaseModel):
    user_name: str
    email: str


class RoomConfig(BaseModel):
    roomName: str
    capacity: int
    rounds: int
    selectedRegion: str
    user_id: int = random.randint(1000, 9999)  # Random user_id for testing


class JoinRoomRequest(BaseModel):
    room_code: str
    region: str
    user_id: int = random.randint(1000, 9999)  # Random user_id for testing
