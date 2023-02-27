def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
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
        "created_at": user["created_at"],
        "password": user["password"]
    }

def userResponseEntity(user) -> dict:
    return { 
        "id": str(user["_id"]),
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
        "created_at": user["created_at"],    
    }
def embeddedUserResponse(user) -> dict:
    return { 
    "id": str(user["_id"]),    
    "phone": user["phone"],
    "email": user["email"],
    "vip": user["vip"],
    "balance": user["balance"],
    "pendingBalance": user["pendingBalance"],
    }

def userListEntity(users) -> list:
    return [userEntity(user) for user in users]