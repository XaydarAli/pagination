import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import User
from schemas.user_schema import UserRegister, UserLogin, UserPasswordReset
from database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from fastapi_pagination import Page, paginate, add_pagination

session = Session(bind=ENGINE)

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get('/', response_model=Page)
async def get_users():
    all_users = session.query(User).all()
    return jsonable_encoder(paginate(all_users))


add_pagination(user_router)


@user_router.get('/auth')
async def get_user(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            user = session.query(User).all()
            return jsonable_encoder(user)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@user_router.post('/login')
async def login_user(user: UserLogin, Authorizotion: AuthJWT = Depends()):
    check_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )).first()
    if check_user and check_password_hash(check_user.password, user.password):
        access_token = Authorizotion.create_access_token(subject=check_user.username,
                                                         expires_time=datetime.timedelta(days=1))
        refresh_token = Authorizotion.create_refresh_token(subject=check_user.username,
                                                           expires_time=datetime.timedelta(days=3))
        data = {
            "success": True,
            "code": 200,
            "message": "Login successful",
            "token": {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password or username")


@user_router.post('/register')
async def register_user(user: UserRegister):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    session.commit()
    data = {
        "status": 201,
        "success": True,
        "message": "User registered",
        "object": {
            "username": user.username,
            "email": user.email,
            "password": generate_password_hash(user.password)
        }
    }
    return jsonable_encoder(data)


@user_router.put('/reset-password')
async def reset_password(user: UserPasswordReset, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        if user.password == user.confirm_password:
            current_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
            if current_user:
                current_user.password = generate_password_hash(user.password)
                session.add(current_user)
                session.commit()

                data = {
                    "code": 200,
                    "success": True,
                    "message": "Password reset"
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
