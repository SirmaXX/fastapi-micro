from pydantic import BaseModel

from typing import Optional

class User_Schema(BaseModel):
   Name:str
   User_name: str
   user_email: str
   Pass: str
   user_status: bool
 
 

    
   class Config:
        from_attributes = True

