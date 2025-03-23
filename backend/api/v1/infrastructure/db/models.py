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
    
    __table_args__ = (
        sa.UniqueConstraint('login', name='uq_user_login'),
        sa.UniqueConstraint('email', name='uq_user_email'),
    )

class Video(Base):
    __tablename__ = 'videos'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    length_seconds: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    size: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    uploaded_at: Mapped[datetime.date] = mapped_column(sa.Date, nullable=False, default=datetime.date.today)    
    author_uuid = mapped_column(sa.ForeignKey('users.uuid'), nullable=False)
    author: Mapped["User"] = relationship(back_populates="videos")
    heat_map: Mapped["HeatMap"] = relationship(back_populates="video")
    
    __table_args__ = (
        sa.UniqueConstraint('name', 'author_uuid', name='uq_video_name_author'),
        sa.ForeignKey(['author_uuid', 'users.uuid'], ondelete='CASCADE', name='fk_video_author'),
    )

class HeatMap(Base):
    __tablename__ = 'heat_maps'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_uuid = mapped_column(sa.ForeignKey('videos.uuid'), nullable=False)
    video: Mapped["Video"] = relationship(back_populates="heat_map")
    
    __table_args__ = (
        sa.UniqueConstraint('video_uuid', name='uq_heat_map_video'),
        sa.ForeignKey(['video_uuid', 'videos.uuid'], ondelete='CASCADE', name='fk_heat_map_video'),
    )