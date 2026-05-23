from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import get_db
from app.models.user import User
from app.models.log import Log
from app.schemas.user import UserResponse, UserBlockRequest
from app.core.dependencies import get_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Получить список всех пользователей (только для ADMIN)"""
    users = db.query(User).all()
    return users


@router.post("/users/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Заблокировать пользователя (только для ADMIN)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
    
    user.is_blocked = True
    db.commit()
    
    return {"message": f"User {user.username} blocked"}


@router.post("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Разблокировать пользователя (только для ADMIN)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_blocked = False
    db.commit()
    
    return {"message": f"User {user.username} unblocked"}


@router.get("/logs")
def get_logs(
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Просмотр журнала действий (только для ADMIN)"""
    logs = (
        db.query(Log)
        .order_by(desc(Log.created_at))
        .limit(limit)
        .all()
    )
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "details": log.details,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat() if log.created_at else None
        }
        for log in logs
    ]


@router.get("/stats")
def get_system_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Системная статистика (только для ADMIN)"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_blocked == False).count()
    blocked_users = db.query(User).filter(User.is_blocked == True).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "blocked_users": blocked_users
    }