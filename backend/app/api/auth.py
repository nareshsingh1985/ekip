from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin",
    },
    "manager": {
        "password": "manager123",
        "role": "Knowledge Manager",
    },
    "business": {
        "password": "business123",
        "role": "Business User",
    },
    "executive": {
        "password": "executive123",
        "role": "Executive",
    },
}


@router.post("/login")
def login(req: LoginRequest):

    user = USERS.get(req.username)

    if (
        user
        and user["password"] == req.password
    ):
        return {
            "success": True,
            "username": req.username,
            "role": user["role"],
        }

    return {
        "success": False
    }