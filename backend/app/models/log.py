from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func

from app.db.base_class import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    action = Column(String, nullable=False)
    
    details = Column(JSON, nullable=True)  # дополнительные данные в JSON
    
    ip_address = Column(String, nullable=True)  # IP-адрес пользователя

    created_at = Column(DateTime(timezone=True), server_default=func.now())