from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from DataBase.room_connection import save_room, add_host_to_room, add_user_details, join_room 
import uuid
import string
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    user_data, is_new = add_user_details(user_name, email, user_id)

    return {
       "status": "success", 
       "data" : user_data,
       "is_new": is_new 
    }

@app.post('/create-room')
def create_room(config: RoomConfig):

    room_id = generate_room_id()
    room_code = generate_room_code()

    print("Generated Room ID: ", room_id)

    save_room(
        room_id,
        room_code,
        config.roomName,
        config.capacity,
        config.rounds,
        config.selectedRegion
    )

    add_host_to_room(room_id, config.user_id)
    is_new = True

    return {
        "message": "Room created successfully",
        "room_id": room_id,
        "room_code": room_code, 
        "is_new" : True 
    }

@app.post('/join-room')

def join_room_endpoint(request: JoinRoomRequest):

    print("Join Code Response: ", end='')
    print(request.room_code, request.region)

    result = join_room(
        request.room_code,
        request.region,
        request.user_id
    )

    print("Result: ", result)
    return result  