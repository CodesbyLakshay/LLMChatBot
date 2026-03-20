from datetime import datetime

from .user import User
from sqlalchemy import Integer, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base


class Document(Base):
    __tablename__ = "document"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"),nullable=False,ondelete="CASCADE")
    file_name: Mapped[str] = mapped_column(String,nullable=False)
    extracted_text: Mapped[Text] = mapped_column(Text,nullable=False)
    uploaded_At: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, )
    user: Mapped[User] = relationship("User")