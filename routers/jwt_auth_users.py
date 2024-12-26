from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# desactualizado en el curo, no es jose es PyJWT, en la docu de fastapi pip install pyjwt
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import settings


secret_key = settings.secret_key


# JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = secret_key

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}
                   )


# OAuth2
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str

users_db = {
    "Delacox": {
        "username": "Delacox",
        "full_name": "Sergio Suarez Prado",
        "email": "sergio@sergio.com",
        "disabled": False,
        "password": "$2a$12$C3jOyrWQp5AhQKWFEvo/bOBM19F6YKGlm53kFfKnFZdrhpxO23FoO"
    },
    "Mouredev": {
        "username": "Mouredev",
        "full_name": "Mouredev",
        "email": "moure@moure.com",
        "disabled": True,
        "password": "$2a$12$C3jOyrWQp5AhQKWFEvo/bOBM19F6YKGlm53kFfKnFZdrhpxO23FoO",
    }
}

# Return user with password
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Return user without password
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])



async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Credenciales de autenticación incorrectas", 
                                headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except jwt.PyJWTError:
        raise exception
    
    return search_user(username)

    


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario deshabilitado")
    return user



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")
    
    # Verify password
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    
    # Verify user status
    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    # Return token
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user