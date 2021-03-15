from sqlalchemy import Column, Integer, String

from config.database import Base
from app.utils.datatype import SqliteNumeric
Numeric = SqliteNumeric


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=True)
    directory = Column(String(191), nullable=True)
    file_extension = Column(String(20), nullable=True)
