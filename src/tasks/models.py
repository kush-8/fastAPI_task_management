from sqlalchemy import Column, String, Boolean, ForeignKey, UUID
import uuid
from src.utils.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)