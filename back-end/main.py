from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import string
import random

from DataBase.schema import init_db
from DataBase.services import register_user_service, create_room_service, join_room_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

class RoomConfig(BaseModel):
    roomName: str
    capacity: int
    rounds: int
    selectedRegion: str
    user_id: int = 1248

class User(BaseModel):
    user_name: str
    email: str

class JoinRoomRequest(BaseModel):
    room_code: str
    region: str
    user_id: int = 1234


def generate_room_id():
    return str(uuid.uuid4())

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.post('/user')
def user(user: User):
    user_name = user.user_name
    email = user.email
    user_id = 1234   

    user_data, is_new = register_user_service(user_name, email, user_id)

    return {
       "status": "success", 
       "data": user_data,
       "is_new": is_new 
    }

@app.post('/create-room')
def create_room(config: RoomConfig):
    room_id = generate_room_id()
    room_code = generate_room_code()

    print("Generated Room ID: ", room_id)

    room_data = create_room_service(
        room_id=room_id,
        room_code=room_code,
        room_name=config.roomName,
        host_id=config.user_id,
        capacity=config.capacity,
        rounds=config.rounds,
        region=config.selectedRegion
    )

    return {
        "message": "Room created successfully",
        "room_id": room_id,
        "room_code": room_code, 
        "room": room_data,
        "is_new": True 
    }

@app.post('/join-room')
def join_room_endpoint(request: JoinRoomRequest):
    result = join_room_service(
        request.room_code,
        request.region,
        request.user_id
    )
    return result
