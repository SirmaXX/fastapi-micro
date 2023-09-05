from pydantic import BaseModel, Field
from typing import Optional



class User_Schema(BaseModel):
    username : str
    password : str
 

    
    class Config:
        orm_mode = True
        validate_assignment = True



class U_User_Schema(BaseModel):
    username : Optional[str]
    password : Optional[str]
 
    class Config:
        orm_mode = True
        validate_assignment = True






   

        




    


    
 