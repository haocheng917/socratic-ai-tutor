from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20,
                          description="用户名长度3-20位")
    password: str = Field(..., min_length=8, max_length=32,
                          description="密码长度8-32位")


class UserLogin(BaseModel):
    username: str
    password: str


class UserMe(BaseModel):
    id: int
    username: str
    credits: int
    membership_plan: str
    membership_expire_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
