from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_delar,
    delete_delar,
    get_delars,
    get_delar_name,
    update_delars
)
from server.models.delars import (
    ResponseModel,
    DelarSchema,
    UpdateDelarSchema,
    ErrorResponseModel
)
from app.auth.auth_handler import signJWT
router = APIRouter()

#Add delar
@router.post("/", response_description="Delar data created")
async def add_new_delar(delar: DelarSchema = Body(...)):
    delar = jsonable_encoder(delar)
    new_delar = await add_delar(delar)
    return ResponseModel(new_delar, "Delar added successfully.")
# Get Delars
@router.get("/", response_description="Delars from database")
async def get_delar_da():
    delars = await get_delars()
    if delars:
        return ResponseModel(delars, "Delars data retrieved successfully")
    return ResponseModel(delars, "Empty list returned")
# Get Delars by name
@router.get("/{name}", response_description="Delar data retrieved")
async def get_delar_data(name):
    delar = await get_delar_name(name)
    if delar:
        return ResponseModel(delar, "Delar Data Retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "Delar doesn't exist")
# Delar update
@router.put("/{name}")
async def update_delar_data(name: str, req: UpdateDelarSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_delar = await update_delars(name, req)
    if updated_delar:
        return ResponseModel(
            "Delar with NAME: {} name update is successfull".format(name),
            "Delar data update successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data"            
        )
# Delar Delate
@router.delete("/{name}",response_description="Delar data deleted" )
async def delete_delar_data(name: str):
    deleted_delar = await delete_delar(name)
    if deleted_delar:
        return ResponseModel(
            "Delar With NAME: {} removed".format(name), "Delar deleted successfully",            
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "Delar with NAME {0} doesn't exist".format(name)
    )
