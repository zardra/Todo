import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


class User(Base, UserMixin):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

    # def delete_user(self):

class Projects(Base):
    __tablename__="projects"
    id = Column(Integer, primary_key=True)
    project_name = Column(String())
    user_id = Column(Integer, ForeignKey("users.id"))

class Tasks(Base):
    __tablename__="tasks"
    id = Column(Integer, primary_key=True)
    task_name = Column(String(150))
    task_status = Column(String(30))
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    # def change_status(self):
    #     status =
    #     return status

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    u = User(email="test@test.com", username="zardra")
    u.set_password("unicorn")
    session.add(u)
    session.commit()

if __name__ == "__main__":
    create_tables()
