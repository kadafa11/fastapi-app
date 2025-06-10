import database as _database
import models as _models
import fastapi.security as _security
import sqlalchemy.orm as _orm
import sys
import os
import schemas as _schemas
from email_validator import validate_email, EmailNotValidError
import fastapi as _fastapi
import passlib.hash as _hash
import jwt as _jwt
_JWT_SECRET="ujdhqowuqw6e9y64570njfkaspi"
oauth2schema=_security.OAuth2PasswordBearer("/api/v1/login")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def create_db():
    return _database.Base.metadata.create_all(bind=_database.engine)

# create_db()
def get_db():
    db=_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create_db();

async def getUserByEmail(email:str, db:_orm.Session):
    return db.query(_models.UserModel).filter(_models.UserModel.email==email).first()

async def create_user(user:_schemas.UserRequest, db:_orm.Session):
    # check for valid email
    try:
         isValid = validate_email(user.email)
         email = isValid.email
    except EmailNotValidError:
            raise _fastapi.HTTPException(status_code=400, detail="Provide valid Email")

    
    # convert normal password to hash form
    hashed_password=_hash.bcrypt.hash(user.password)
    # create the user model to be saved in database
    user_obj=_models.UserModel(
        email=email,
        name=user.name,
        phone=user.phone,
        password_hash=hashed_password
    )
    # save the user in the db
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def create_token(user:_models.UserModel):
    # convert user model to user schema
    user_schema=_schemas.UserResponse.from_orm(user)
    print(user_schema)
    # convert object to dictionary
    user_dict=user_schema.dict()
    del user_dict["created_at"]

    token=_jwt.encode(user_dict,_JWT_SECRET)

    return dict(access_token=token,token_type="bearer")


async def login(email:str,password:str,db:_orm.Session):
    db_user=await getUserByEmail(email=email,db=db)

    # RETURN FALSE IF USER WITH NO EMAIL FOUND

    if not db_user:
        return False
    
    # RETURN FALSE IF USER WITH NO password FOUND
    if not db_user.password_verification(password=password):
        return False
    
    return db_user

async def current_user(db:_orm=_fastapi.Depends(get_db),
                       token:str=_fastapi.Depends(oauth2schema)):
    try:
        payload=_jwt.decode(token,_JWT_SECRET,algorithms=["HS256"])
        # Get User by ID
        db_user=db.query(_models.UserModel).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401,detail="Wrong Credentials")

    #If all okay then return the DTO?Schema version User
    return _schemas.UserResponse.from_orm(db_user)

async def create_post(user:_schemas.UserResponse,db:_orm.Session,
                      post:_schemas.PostRequest):
    post= _models.PostModel(**post.dict(), user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    # Convert the Post model to Post DTO/Schema and return to API layer
    return _schemas.PostResponse.from_orm(post)

async def get_posts_by_user(user:_schemas.UserResponse ,db:_orm.Session):
    posts=db.query(_models.PostModel).filter_by(user_id=user.id)

    # CONVERT EACH POST MODEL TO POST SCHEMA AND MAKE A LIST TO BE RETURNED
    return list(map(_schemas.PostResponse.from_orm,posts))


async def get_posts_by_all(db:_orm.Session):
    posts=db.query(_models.PostModel)

    # CONVERT EACH POST MODEL TO POST SCHEMA AND MAKE A LIST TO BE RETURNED
    return list(map(_schemas.PostResponse.from_orm,posts))



async def get_post_detail(post_id:int,db:_orm.Session):
    db_post=db.query(_models.PostModel).filter(_models.PostModel.id==post_id).first()
    if db_post is None:
        raise _fastapi.HTTPException(status_code=404,detail="Post not found")

    # return _schemas.PostResponse.from_orm(db_post)
    return db_post

async def get_user_detail(user_id:int,db:_orm.Session):
    db_user=db.query(_models.UserModel).filter(_models.UserModel.id==user_id).first()
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404,detail="User not found")

    return _schemas.UserResponse.from_orm(db_user)
    

async def delete_post(post:_models.PostModel,db:_orm.Session):
    db.delete(post)
    db.commit()

async def update_post(
        post_request: _schemas.PostRequest,
        post: _models.PostModel,
        db: _orm.Session
):
    post.post_title=post_request.post_title
    post.post_description=post_request.post_description
    post.image=post_request.image

    db.commit()
    db.refresh(post)

    return _schemas.PostResponse.from_orm(post)



