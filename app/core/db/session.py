import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings


SQLALCHEMY_DATABASE_URL = "mysql://{}:{}@{}/{}".format(
    settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_HOST, settings.DATABASE_NAME,
)

pymysql.install_as_MySQLdb()

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionGlobal = sessionmaker(autocommit=True, autoflush=True, bind=engine)
SessionScoped = scoped_session(SessionLocal)
