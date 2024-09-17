from fastapi import status, Depends, APIRouter, HTTPException
from database import ENGINE, Session
from models import User, Post, Comments
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from schemas.comment_schema import CommentUpdateModel, CommentCreateModel
from fastapi_pagination import Page, paginate, add_pagination

session = Session(bind=ENGINE)

comment_router = APIRouter(prefix="/comments", tags=["Comments"])


@comment_router.get('/', response_model=Page)
async def get_comment():
    all_comments = session.query(Comments).all()
    return jsonable_encoder(paginate(all_comments))


add_pagination(comment_router)


@comment_router.post("/create")
async def create_comment(comment: CommentCreateModel, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            new_comment = Comments(
                content=comment.content,
                user_id=check_user.id,
                post_id=comment.post_id,
            )
            session.add(new_comment)
            session.commit()

            data = {
                "code": 200,
                "success": True,
                "message": f"comment is written by {check_user.username}",
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@comment_router.put("/{id}")
async def update_comment(id: int, post: CommentUpdateModel, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            check_comment = session.query(Comments).filter(Comments.id == id).first()
            if check_comment:
                for key, value in post.dict().items():
                    setattr(check_comment, key, value)

                    data = {
                        "code": 200,
                        "success": True,
                        "message": "Post is updated succesfully",
                        "object": {
                            "content": check_comment.content,
                            "user_id": check_user.id,
                            "post_id": check_comment.post_id,
                        }
                    }
                    session.add(check_comment)
                    session.commit()
                    return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@comment_router.delete("/{id}")
async def delete_comment(id: int, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        if check_user:
            comment = session.query(Post).filter(Post.id == id).first()
            if comment:
                session.delete(comment)
                session.commit()
                return jsonable_encoder({"code": 200, "message": "comment is deleted successfully"})
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
