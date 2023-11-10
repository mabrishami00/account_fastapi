from fastapi import APIRouter,  Request, status, HTTPException, Header, Depends
from fastapi.responses import JSONResponse

from db.mongodb import collection
from db.redis import get_redis
from schemas.users import UserCreate, UserLogin, UserLoginOTP
from .utils import validate_user_registration
from .backends import jwt_authentication
from core.config import settings

from my_simple_jwt_auth.my_simple_jwt_auth import jwt_authentication
import httpx
import json

router = APIRouter(prefix="/account")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(user_data: UserCreate):
    user_data_dict = user_data.model_dump()
    username_exist, email_exist = await validate_user_registration(collection, user_data_dict)
    if username_exist and email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and email has been existed.")
    elif username_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username has been existed.")
    elif email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email has been existed.")

    result = await collection.insert_one(user_data_dict)
    return str(result.inserted_id)
