from sqlalchemy import or_
from models import User, Post
from database import Session, ENGINE
from routers.user_router import user_router
from routers.post_router import post_router
from routers.comment_router import comment_router
from schemas.user_schema import Settings
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)


@app.get("/")
async def root():
    return {"message":Welcome ""}


@app.get("/{username}")
async def get_user_page(username: str, authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        current_user = Session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject()
            )).first()
        if current_user:
            other_user = Session.query(User).filter(User.username == username).first()
            if other_user:
                data = {
                    "success": True,
                    "code": 200,
                    "message": f"{other_user.username} profile page",
                }
                return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{username} not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{username} not found")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
