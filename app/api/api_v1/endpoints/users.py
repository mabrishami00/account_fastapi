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


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user_data: UserLogin, redis=Depends(get_redis)):
    username = user_data.username
    password = user_data.password
    result = await collection.find_one({"username": username, "password": password})
    if result:
        access_token, refresh_token, jti = jwt_authentication.generate_access_and_refresh_token(username, settings.ACCESS_KEY_EXPIRE_TIME, settings.REFRESH_KEY_EXPIRE_TIME, settings. SECRET_KEY)
        await redis.set(jti, username)
        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/login_otp", status_code=status.HTTP_200_OK)
async def user_login_otp(user_data: UserLoginOTP):
    username = user_data.username
    print(username)
    user = await collection.find_one({"username": username})
    if user:
        async with httpx.AsyncClient() as client:
            url = settings.SEND_OTP_URL
            data = {"email": user.get("email")}
            response = await client.post(url, json=data)
            response_text = json.loads(response.text)
            if response.status_code == 200:
                return JSONResponse(response_text)
            else:
                return JSONResponse(response_text, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return JSONResponse({"detail": "You have not been registered yet."}, status_code=status.HTTP_401_UNAUTHORIZED)

