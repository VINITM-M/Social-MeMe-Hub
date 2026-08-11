import uuid
import string
import random
from fastapi import APIRouter
from app.schemas.room_schema import RoomConfig, JoinRoomRequest
from app.services.room_service import create_room_service, join_room_service

router = APIRouter()

def generate_room_id():
    return str(uuid.uuid4())

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@router.post('/create-room')
def create_room(config: RoomConfig):
    #room_id Creation along with room_code
    room_id = generate_room_id()
    room_code = generate_room_code()

    room_data = create_room_service(
        room_id,
        room_code,
        config.roomName,
        config.user_id,
        config.capacity,
        config.rounds,
        config.selectedRegion
    )
    #room-link generation
    room_link = f"http://localhost:3000/join/{room_id}/{config.selectedRegion}/{room_code}"

    return {
        "message": "Room created successfully",
        "room_id": room_id,
        "room_code": room_code,
        "room": room_data,
        "is_new": True,
        "room_link": room_link
    }


@router.post('/join-room')
def join_room_endpoint(request: JoinRoomRequest):
    result = join_room_service(
        request.room_code,
        request.region,
        request.user_id
    )
    return result
