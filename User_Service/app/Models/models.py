import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,DateTime,String,Integer, ForeignKey, Table 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker,relationship 
from sqlalchemy.sql import expression
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date
from datetime import datetime


DB_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DB_URL,
    pool_size=5,
    pool_recycle=60,
    pool_pre_ping=True)

SessionLocal = sessionmaker( bind=engine,
    autocommit=False,
    autoflush=False)

session=SessionLocal()
Base = declarative_base() 
Now = datetime.utcnow()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_reset():
   """Veritabanını sıfırlamak için hazırlan fonksiyon """
   Base.metadata.reflect(bind=engine)
   Base.metadata.drop_all(bind=engine)
   




# Define the Permissions table
class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(255), nullable=False, unique=True)

    # Define the relationship to roles with a foreign key
    role_id = Column(Integer, ForeignKey('Roles.role_id'))
    role = relationship("Role", back_populates="permissions")



# Define the Roles table
class Role(Base):
    __tablename__ = 'Roles'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(255), nullable=False, unique=True)

    # Define the relationship to permissions with a foreign key
    permissions = relationship("Permission", back_populates="role")
    # Define the users relationship
    users = relationship("User", back_populates="role")



# Define the User table
class User(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    User_name = Column(String(255), nullable=False, unique=True)
    user_email = Column(String(255), nullable=False, unique=True)
    Pass = Column(String(255), nullable=False)
    user_status = Column(Boolean, unique=False, default=True)  
    insert_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Define the role_id as a foreign key
    role_id = Column(Integer, ForeignKey('Roles.role_id'))

    # Define the roles relationship
    role = relationship("Role", back_populates="users")




# Create a Role object
role = Role(
    role_name="Admin"
)

# Create a Permission object
permission = Permission(
    permission_name="Create User"
)




# Create instances of your model classes
user1 = User(Name="User1", User_name="user1", user_email="user1@example.com", Pass="password123")
user2 = User(Name="User2", User_name="user2", user_email="user2@example.com", Pass="password456")

role1 = Role(role_name="Admin")
role2 = Role(role_name="User")

permission1 = Permission(permission_name="Edit")
permission2 = Permission(permission_name="View")

# Assign roles and permissions to users (modify this part as needed)
user1.role = role1
user2.role = role2

role1.permissions = [permission1]
role2.permissions = [permission2]


db_reset()
Base.metadata.create_all(bind=engine)
session.add(user1)
session.add(user2)
session.add(role1)
session.add(role2)
session.add(permission1)
session.add(permission2)
session.commit()
