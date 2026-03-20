import datetime
from app.database import Base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email: Mapped[str] = mapped_column(String,nullable=False,unique=True,index=True)
    hashed_password:Mapped[str] = mapped_column(String,nullable=False)
    created_At:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False,)