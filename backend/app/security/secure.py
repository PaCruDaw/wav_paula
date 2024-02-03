
from jose import jwt, JWTError
from app.utils import config
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, SecurityScopes 
from passlib.context import CryptContext
from app.models.data.sqlalchemy_models import Users
from app.models.requests.tokens import TokenData
from fastapi import Depends, HTTPException, status, Security
from app.db_config.database import get_db
from sqlalchemy.orm import Session
from app.repository.login import LoginRepository

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",  
    scopes={"user": "Read information about the current user.", "items": "Read items."},
    )
def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

def authenticate(username, password, account:Users):
    try:
        password_check = verify_password(password, account.password)
        return password_check
    except Exception as e:
        print(e)
        return False
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password):
    return crypt_context.hash(password)

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), sess:Session = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception
    loginrepo = LoginRepository(sess)
    user = loginrepo.get_all_login_username(token_data.username)
 
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

def get_current_valid_user(current_user: Users = Security(get_current_user, scopes=["user"])):
    if current_user == None:
        raise HTTPException(status_code=400, detail="Invalid user")
    return current_user