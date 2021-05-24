from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship

from .db import db
from resources.crud import CRUDModel

class Parking(db.Model, CRUDModel):
    __tablename__ = 'parkings'

    id = Column(Integer, primary_key=True, server_default=text("nextval('parkings_parking_id_seq'::regclass)"))
    name = Column(String(50), nullable=False)
    description = Column(Text)
    address = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


class User(db.Model, CRUDModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)


class Bookmark(db.Model, CRUDModel):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True, server_default=text("nextval('bookmarks_bookmark_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    parking_id = Column(ForeignKey('parkings.id'), nullable=False)

    parking = relationship('Parking')
    user = relationship('User')


class Camera(db.Model, CRUDModel):
    __tablename__ = 'cameras'

    id = Column(Integer, primary_key=True, server_default=text("nextval('cameras_camera_id_seq'::regclass)"))
    parking_id = Column(ForeignKey('parkings.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    is_available = Column(Boolean, nullable=False)

    parking = relationship('Parking')


class Lot(db.Model, CRUDModel):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True, server_default=text("nextval('lots_lot_id_seq'::regclass)"))
    camera_id = Column(ForeignKey('cameras.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    side = Column(Integer, nullable=False)

    camera = relationship('Camera')


class Status(db.Model, CRUDModel):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, server_default=text("nextval('status_status_id_seq'::regclass)"))
    lot_id = Column(ForeignKey('lots.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    is_free = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)

    lot = relationship('Lot')
