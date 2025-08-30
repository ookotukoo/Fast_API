from fastapi import FastAPI

from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()

data = {
    "email": "abc@mail.ru",
    "bio": "Привет!",
    "age": 12
}

data_wo_age = {
    "email": "abc@mail.ru",
    "bio": "Привет!",
    "gender": "male",
    "birthday": "2022"
}


class UserSchem(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra="forbid")

users = []

@app.post("/users")
def add_user(user: UserSchem):
    users.append(user)
    return {"ok": True, "msg": "Пользователь добавлен"}


@app.get("/users")
def get_users() -> list[UserSchem]:
    return users

#
# class UserAgeSchem(UserSchem):
#     age: int = Field(ge=0, le=100)

#
# print(repr(UserSchem(**data_wo_age)))
# print(repr(UserAgeSchem(**data)))