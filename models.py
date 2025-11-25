from database import Base
from sqlalchemy import Column, String, Boolean, Integer
from database import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

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
    
    # Foreign key to the User Table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Many-to-One relationship
    owner = relationship("User", back_populates="todos")
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_pass = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    # One-to-Many relationship
    todos = relationship(
        "TODO",
        back_populates="owner",
        cascade="all, delete-orphan"
    )