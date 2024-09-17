import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import Likes, User
from schemas.user_schema import UserRegister, UserLogin, UserPasswordReset
from database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

session = Session(bind=ENGINE)

like_router = APIRouter(prefix="/likes", tags=["likes"])

@like_router.get("/likes")
async def get_likes(authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()

        current_user = session.query(User).filter(
            or_(
                User.username == authorization.get_jwt_subject(),
                User.email == authorization.get_jwt_subject()
            )).first()
        if current_user:
            likes = session.query(Likes).all()
            return jsonable_encoder(likes)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not logged in")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

