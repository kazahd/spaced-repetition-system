from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_current_user,
    get_admin_user
)

from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/admin")
def admin_only(
    admin: User = Depends(get_admin_user)
):
    return {
        "message": f"Hello admin {admin.username}"
    }