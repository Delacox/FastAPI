from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Documentacion auto
# https://api-c3bu.onrender.com/docs
# https://api-c3bu.onrender.com/redoc




# Routers 
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="/static")

@app.get("/")
async def root():
    return "Hola!"

@app.get("/url")
async def url():
    return { "url":"https://mouredev.com/python" }
