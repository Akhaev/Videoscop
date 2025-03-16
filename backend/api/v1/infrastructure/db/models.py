import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(sa.String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    videos: Mapped[list["Video"]] = relationship(back_populates="author")
    
class Video(Base):
    __tablename__ = 'videos'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    length_seconds: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    size: Mapped[str] = mapped_column(sa.String(10), nullable=False)
    uploaded_at: Mapped[datetime.date] = mapped_column(sa.Date, nullable=False, default=datetime.date.today)    
    author_uuid = mapped_column(sa.ForeignKey('users.uuid'), nullable=False)
    author: Mapped["User"] = relationship(back_populates="videos")
    heat_map: Mapped["HeatMap"] = relationship(back_populates="video")
    

class HeatMap(Base):
    __tablename__ = 'heat_maps'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    heat_map_data: Mapped[dict] = mapped_column(sa.JSON, nullable=False)
    video_uuid = mapped_column(sa.ForeignKey('videos.uuid'), nullable=False)
    video: Mapped["Video"] = relationship(back_populates="heat_map")