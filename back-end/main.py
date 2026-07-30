from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import string
import random

from DataBase.schema import init_db
from DataBase.services import register_user_service, create_room_service, join_room_service
from DataBase.user_db import get_user_by_email, create_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Login(BaseModel):
    email_id: str
    password: str 

class Signup(BaseModel): 
    first_name: str
    last_name: str
    email_id: str
    password: str 
class RoomConfig(BaseModel): 
    roomName: str
    capacity: int
    rounds: int
    selectedRegion: str
    user_id: int = random.randint(1000, 9999)  # Random user_id for testing
class User(BaseModel):
    user_name: str
    email: str 
class JoinRoomRequest(BaseModel):
    room_code: str
    region: str
    user_id: int = random.randint(1000, 9999)  # Random user_id for testing


def generate_room_id():
    return str(uuid.uuid4())

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  

@app.post('/login') 
def login(login_details: Login):
    print(f"Received login details: {login_details}") 

@app.post('/signup')
def signup(sign_details: Signup): 

    user_data, boolean = register_user_service(sign_details.first_name + " " + sign_details.last_name, sign_details.email_id, sign_details.password) 
    if not boolean:
        return {
            "message": "User already exists",
            "user": user_data,
            "is_registered": False
        } 
    else: 
        return {
            "message": "User registered successfully", 
            "user": user_data,
            "is_registered": True
        }

@app.post('/create-room')
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

@app.post('/join-room')
def join_room_endpoint(request: JoinRoomRequest):
    
    result = join_room_service(
        request.room_code,
        request.region,
        request.user_id
    )
    return result


@app.post('/user')
def create_or_get_user(user: User):
   
    existing = get_user_by_email(user.email)
    if existing:
        return {"data": existing, "is_new": False}

    new_user = create_user(user.user_name, user.email, "")
    return {"data": new_user, "is_new": True}
