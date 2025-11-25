from database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, text
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
import uuid

class TODO(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=True)
    complete = Column(Boolean, nullable=False, default=False)
    # createdAt = Column(TIMESTAMP(timezone=True),
    #                    nullable=False, server_default=func.now())
    # updatedAt = Column(TIMESTAMP(timezone=True),
    #                    default=None, onupdate=func.now())