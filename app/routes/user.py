from datetime import timedelta
from fastapi import APIRouter, Body, Response, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from helper.time_helper import Timez
from helper.email_helper import sendMail
from helper.sms_helper import send_msg
from bson.objectid import ObjectId
from server.database import (
    add_user,
    delete_user,
    get_users,
    get_user_id,
    update_users
)
from server.models.user import (
    ResponsModels,
    UserSchema,
    UpdateUserModel
)
from app.auth.auth_handler import signJWT
from helper.number_helper import random_with_N_digits
from app.auth.oauth2 import AuthJWT
from server.database import users_collection
from app.serializers.userSerialozers import userEntity,userResponseEntity
from .. import utils
from server.models.user import ( UserResponse , CreateUserSchema, LoginUserSchema) 
from decouple import config
from app.auth import oauth2


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = float(config("ACCESS_TOKEN_EXPIRES_IN"))
REFRESH_TOKEN_EXPIRES_IN = float(config("REFRESH_TOKEN_EXPIRES_IN"))

# Add user
@router.post("/", response_description="User data created")
def add_new_user(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user =  add_user(user)
    return ResponsModels.ResponseModel(new_user, "User added successfully.")
# Get Users
@router.get("/", response_description="Users form database")
def get_users_da():
    users = get_users()
    if users:
        return ResponsModels.ResponseModel(users, "users data retrieved successfully")
    return ResponsModels.ResponseModel(users, "Empty list returned")
# Get User by ID
@router.get("/{id}", response_description="User data retrieved")
def get_user_data(id: int):
    user = get_user_id(id)
    if user:
        return ResponsModels.ResponseModel(user, "User Data Retrieved successfully")
    return ResponsModels.ErrorResponseModel("An error occurred", 404, "User doesn't exist")
# User Update
@router.put("/{id}")
def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = update_users(id, req)
    if updated_user:
        return ResponsModels.ResponseModel(
            "User with ID: {} name update is successfull".format(id),
            "User data update successfully",
        )
    return ResponsModels.ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data"
    )
# User Delete 
@router.delete("/{id}", response_description="User data deleted")
def delete_user_data(id: str):
    deleted_user = delete_user(id)
    if deleted_user:
        return ResponsModels.ResponseModel(
            "User With ID: {} removed".format(id), "User deleted successfully",

        )
    return ResponsModels.ErrorResponseModel(
        "An error occurred",
        404,
        "User with ID {0} doesn't exist".format(id)
    )
# Registe
@router.post('/register', status_code= status.HTTP_201_CREATED, response_model=UserResponse)
async def create_n_user(payload: CreateUserSchema):
    # Check if user already exist
    user = users_collection.find_one({'email': payload.email.lower()})
    print(user)
    if user:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT,
        detail='Account already exist')
    #compare password and passwordConfirm
    if payload.password != payload.password_confirm:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail='Passwords do not match'
            )
    # Hash the password
    payload.password = utils.hash_password(payload.password)
    del payload.password_confirm
    m = random_with_N_digits(6)
    payload.email_code = m
    sendMail(receiver_email= payload.email, sub="تفعيل حسابك", asd= f"رمز التفعيل الخاص بكم هو\n{m}")
    s = random_with_N_digits(5)
    payload.sms_code = s
    send_msg(job_name="تفعيل رقم", msg=f"{s} رمز تفعيلكم هو", to = f"963{payload.phone}")
    payload.vip = 0
    payload.balance = 0
    payload.pendingBalance = 0
    payload.created_at = Timez.time_now()
    payload.email = payload.email.lower()
    payload.location = payload.location.lower()
    result = users_collection.insert_one(payload.dict())
    new_user = userResponseEntity(users_collection.find_one({'_id': result.inserted_id}))
    return {"status": "success", "user": new_user}
# Login USER

@router.post('/login')
def login(payload: LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    # Check if the user exist
    db_user = users_collection.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = userEntity(db_user)

    # Check if the password is valid
    if not utils.verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(days=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token}


@router.get('/refresh')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = userEntity(users_collection.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}