from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={404:{"message": "Not found"}}
                   )

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="John", surname="Doe", url="https://johndoe.com", age=30),
         User(id=2, name="John", surname="Doe", url="https://johndoe.com", age=30),
         User(id=3, name="John", surname="Doe", url="https://johndoe.com", age=30)]

@router.get("/")
async def users():
    return users_list


# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user_by_id(id)

# Query
@router.get("/userquery/")
async def user(id: int):
    return search_user_by_id(id)
    
 
# Post
@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user_by_id(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
        
    else:
        users_list.append(user)

# Put
@router.put("/user/")
async def user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
    return

# Delete
@router.delete("/user/{id}")
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            
    
    

     
    
# Function search user
def search_user_by_id(id: int):
    try:
        return next((user for user in users_list if user.id == id))
    except:
        return {"error": "Usuario no encontrado"}