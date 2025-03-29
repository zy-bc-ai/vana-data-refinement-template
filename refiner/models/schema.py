from typing import Optional
from pydantic import BaseModel

class Schema(BaseModel):
    name: str
    version: str
    description: str
    dialect: str
    schema: str