from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}
                   )



oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234"
    },
    "Mouredev": {
        "username": "Mouredev",
        "full_name": "Mouredev",
        "email": "moure@moure.com",
        "disabled": True,
        "password": "1234",
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


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail="Credenciales de autenticación incorrectas", 
                                    headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario deshabilitado")
    return user
    
    

    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")
    if form.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    return {"access_token": user.username, "token_type": "bearer"}
    
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user