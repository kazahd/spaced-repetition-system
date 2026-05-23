from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt

from app.db.database import SessionLocal
from app.models.log import Log
from app.core.config import settings


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Обрабатываем запрос
        response = await call_next(request)
        
        # Логируем только методы, которые изменяют данные
        if request.method in ["POST", "PUT", "DELETE"]:
            db = SessionLocal()
            try:
                # Пытаемся получить user_id из JWT токена
                user_id = None
                auth_header = request.headers.get("Authorization")
                
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.replace("Bearer ", "")
                    try:
                        payload = jwt.decode(
                            token,
                            settings.SECRET_KEY,
                            algorithms=[settings.ALGORITHM]
                        )
                        user_id = int(payload.get("sub")) if payload.get("sub") else None
                    except:
                        pass  # Невалидный токен или не удалось декодировать
                
                # Создаём запись в логе
                log = Log(
                    user_id=user_id,
                    action=f"{request.method} {request.url.path}",
                    ip_address=request.client.host if request.client else None
                )
                db.add(log)
                db.commit()
            except Exception as e:
                print(f"Logging error: {e}")
            finally:
                db.close()
        
        return response