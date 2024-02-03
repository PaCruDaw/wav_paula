from fastapi import APIRouter, Depends, HTTPException, Security, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.services.login import LoginService
from app.models.requests.login import LoginReq,UserCreate
from app.security.secure import authenticate, create_access_token
import re
from datetime import datetime, timedelta

router = APIRouter()

pattern_email =  r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@router.post('/account',response_model=LoginReq)
def login_app(user:LoginReq, loginservice:LoginService = Depends(LoginService)):
    
    login = loginservice.get_login(user.username)
    if login is None:
        return JSONResponse(status_code=404, content="User not found")
    return jsonable_encoder(login)

@router.post('/register')
def login_app(user:UserCreate, loginservice:LoginService = Depends(LoginService)):    
    if re.match(pattern_email, user.email):
        login = loginservice.create_user(user)
        if not login:
            return JSONResponse(status_code=500, content="User not created")
    else:
        return JSONResponse(content={'message':'email is not valid'}, status_code=401)
    return jsonable_encoder(login)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
@router.post("/token")
def access_token(user:LoginReq, loginservice:LoginService = Depends(LoginService)):
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    account = loginservice.get_login(user.username)
    if authenticate(user.username, user.password, account):
        access_token = create_access_token(
            data={"sub": user.username, "scopes": ['user']},
            expires_delta=access_token_expires,
        )
    
        return {
            "access_token": access_token,
            "expires_in": access_token_expires,
            "token_type": "Bearer",
            "userid": user.username,
            "scope": "SCOPE"
           
        }
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect credentials")