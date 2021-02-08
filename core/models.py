from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, VARCHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os

from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class ConnectionToPLC(BaseModel):
    __tablename__ = 'connections'

    name = Column(VARCHAR(255), nullable=False, unique=True)
    ip = Column(VARCHAR(255), nullable=False)
    port = Column(Integer, default=102, nullable=True)
    description = Column(VARCHAR(255), nullable=True)


class RowOneData(BaseModel):
    """табилца для хранения данных одиночного выбора значения из PLC"""
    __tablename__ = 'data_one'

    connections_id = Column(Integer, ForeignKey('connections.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(VARCHAR(255), unique=True)
    start_address = Column(Integer, nullable=False)
    offset = Column(Integer, nullable=False)


class RowManyData(BaseModel):
    """Таблица хранения данных для массовой выгрузки значений из PLC"""
    __tablename__ = 'data_many'

    connections_id = Column(Integer, ForeignKey('connections.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    start_address = Column(Integer, nullable=False)
    offset = Column(Integer, nullable=False)

class DataInMany(BaseModel):
    """таблица для извлечения данных из байт массива полученным из RowManyData"""
    __tablename__ = 'row_in_many'

    manydata_id = Column(Integer, ForeignKey('data_many.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    start_address = Column(Integer, nullable=False)
    offset = Column(Integer, nullable=False)