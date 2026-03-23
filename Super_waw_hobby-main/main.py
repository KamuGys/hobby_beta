from fastapi import FastAPI
from routers import posts, auth

app = FastAPI(title="HobbyX API")

#app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "HobbyX API — работает"}