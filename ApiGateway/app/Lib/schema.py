from pydantic import BaseModel

from typing import Optional

class User_Schema(BaseModel):
    username : str
    password : str
 

    
    class Config:
        orm_mode = True

