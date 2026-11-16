from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20,
                          description="用户名长度3-20位")
    password: str = Field(..., min_length=8, max_length=32,
                          description="密码长度8-32位")


class UserLogin(BaseModel):
    username: str
    password: str
