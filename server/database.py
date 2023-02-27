from pymongo import mongo_client
import pymongo
from bson.objectid import ObjectId
from decouple import config
MONGO_DETAILS = config("MONGO_DETAILS")

client = mongo_client.MongoClient(MONGO_DETAILS)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")


database = client.cashv1
users_collection = database.get_collection("users")
delar_collection = database.get_collection("delar")

# helper

def users_helper(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "id": user["id"],
        "firstname": user["firstname"],
        "middlename": user["middlename"],
        "lastname": user["lastname"],
        "username": user["username"],
        "phone": user["phone"],
        "email": user["email"],
        "location": user["location"],
        "vip": user["vip"], 
        "phoneVerfication": user["phoneVerfication"],
        "emailVerfication": user["emailVerfication"],
        "balance": user["balance"],
        "pendingBalance": user["pendingBalance"],
        "sms_code": user["sms_code"],
        "email_code": user["email_code"],
        "created_at": user["created_at"]
    }
def delar_helper(delar) -> dict:
    return {
        "_id": str(delar["_id"]),
        "name": delar["name"],
        "location": delar["location"],
        "state": delar["state"],
        "phone": delar["phone"]
    }

#User
# Retrieve all Users
def get_users():
    users = []
    for user in users_collection.find():
        users.append(users_helper(user))
    return users
#Delar
# Retrieve all
def get_delars():
    delars = []
    for delar in delar_collection.find():
        delars.append(delar_helper(delar))
    return delars
#User
# Add a new Users
def add_user(user_data: dict) -> dict:
    user =  users_collection.insert_one(user_data)
    new_user =  users_collection.find_one({"_id": user.inserted_id})
    return users_helper(new_user)
#Delar
# Add a new Delar
def add_delar(delar_data: dict) -> dict:
    delar =  delar_collection.insert_one(delar_data)
    new_delar =  delar_collection.find_one({"_id": delar.inserted_id})
    return delar_helper(new_delar)
#User
# Get user with a matching ID
def get_user_id(id: int) -> dict:
    user =  users_collection.find_one({"id": id})
    if user:
        return users_helper(user)
#Delar
def get_delar_name(name: str) -> dict:
    delar =  delar_collection.find_one({"name": name})
    if delar:
        return delar_helper(delar)
#User        
# Update a user with a matching ID
def update_users(id: str, data: dict):
    if len(data) < 1 :
        return False
    user =  users_collection.find_one({"id": id})
    if user:
        update_user =  users_collection.update_one(
            {"id": id}, {"$set": data}
        )
        if update_user:
            return True
        return False
#Delar
def update_delars(name: str, data: dict):
    if len(data) < 1 :
        return False
    delar =  delar_collection.find_one({"name": name})
    if delar :
        update_delar =  delar_collection.update_one(
            {"name": name}, {"$set": data}
        )
        if update_delar:
            return True
        return False
#User
# Delete a user
def delete_user(id: str):
    user =  users_collection.find_one({"id": id})
    if user:
         users_collection.delete_one({"id": id})
    return True
#Delar
def delete_delar(name: str):
    delar =  delar_collection.find_one({"name": name})
    if delar:
         delar_collection.delete_one({"name": name})
    return True

