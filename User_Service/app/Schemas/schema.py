from pydantic import BaseModel, Field
from datetime import datetime
from typing import List





# Pydantic schema for Role
class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    role_id: int

    class Config:
        from_attributes = True

# Pydantic schema for Permission
class PermissionBase(BaseModel):
    permission_name: str

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    permission_id: int

    class Config:
        from_attributes = True


# Pydantic schema for UserRole
class UserRoleBase(BaseModel):
    user_id: int
    role_id: int

class UserRoleCreate(UserRoleBase):
    pass

class UserRole(UserRoleBase):
    class Config:
        from_attributes = True

# Pydantic schema for User
class UserBase(BaseModel):
    Name: str
    User_name: str
    user_email: str
    Pass: str
    user_status: bool

class UserCreate(UserBase):
    pass

class User(UserBase):
    ID: int
    insert_date: datetime = Field(default_factory=datetime.utcnow)
    update_date: datetime = Field(default_factory=datetime.utcnow)
    roles: List[UserRole] = []

    class Config:
        from_attributes = True