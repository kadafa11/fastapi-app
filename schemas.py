
import pydantic as _pydantic
import datetime as _datetime

class UserBase(_pydantic.BaseModel):
    email: str
    name: str
    phone: str

    class Config:
        from_attributes = True

class UserRequest(UserBase):
    password: str

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    created_at: _datetime.datetime

    class Config:
        from_attributes = True

class PostBase(_pydantic.BaseModel):
    post_title: str
    post_description: str
    image: str

    class Config:
        from_attributes = True

class PostRequest(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: _datetime.datetime

    class Config:
        from_attributes = True
