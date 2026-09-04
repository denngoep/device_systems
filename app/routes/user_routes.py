from typing import Literal

from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.user_schema import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# Base de datos simulada en memoria
users = [
    {
        "id": 1,
        "name": "Valentina Garcia",
        "email": "valentina@example.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Marcela Oliveros",
        "email": "marcela@example.com",
        "role": "support",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Dayana Buelvas",
        "email": "dayana@example.com",
        "role": "user",
        "is_active": False
    }
]


@router.get("", response_model=list[UserResponse])
def get_users(
    response: Response,
    role: Literal["admin", "support", "user"] | None = None,
    is_active: bool | None = None
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    filtered_users = users

    if role is not None:
        filtered_users = [
            user for user in filtered_users
            if user["role"] == role
        ]

    if is_active is not None:
        filtered_users = [
            user for user in filtered_users
            if user["is_active"] == is_active
        ]

    return filtered_users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for existing_user in users:
        if existing_user["email"].lower() == user.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este correo"
            )

    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    users.append(new_user)

    return new_user