from DataBase.user_db import get_user_by_email, create_user
from DataBase.room_db import create_room, get_room_by_code_and_region, increment_room_players
from DataBase.members import add_host, add_player, is_member, count_members

def register_user_service(user_name, email, user_id):
    user = get_user_by_email(email)
    if user:
        return user, False
    new_user = create_user(user_id, user_name, email)
    return new_user, True

def create_room_service(room_id, room_code, room_name, capacity, rounds, region, host_id):
    room = create_room(room_id, room_code, room_name, host_id, capacity, rounds, region)
    add_host(room_id, host_id)
    return room

def join_room_service(room_code, region, user_id):
    room = get_room_by_code_and_region(room_code, region)
    if not room:
        return {
            "status": "error",
            "message": "Room not found"
        }

    room_id = room['room_id']
    capacity = room['capacity']
    current_cnt = count_members(room_id)

    if is_member(room_id, user_id):
        return {
            "status": "success",
            "message": "User already in room",
            "presentIn": current_cnt,
            "capacity": capacity,
            "remainingCapacity": max(0, capacity - current_cnt),
            "room": room
        }

    if current_cnt >= capacity:
        return {
            "status": "error",
            "message": "Room is full",
            "presentIn": current_cnt,
            "capacity": capacity,
            "remainingCapacity": 0,
            "room": room
        }

    add_player(room_id, user_id)
    increment_room_players(room_id)
    new_cnt = current_cnt + 1

    return {
        "status": "success",
        "message": "Joined room successfully",
        "presentIn": new_cnt,
        "capacity": capacity,
        "remainingCapacity": max(0, capacity - new_cnt),
        "room": room
    }