from typing import Optional
from sqlmodel import Field, Session, SQLModel, select

class TeamBase(SQLModel):
    name: str = Field(index=True)
    

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    """
    It's a data model
    It's a Pydantic model because it doesn't create a
    table in database
    It's used to declare only data schemas for the api
    """
    pass

class HeroRead(HeroBase):
    """
    It's a data model
    It's a Pydantic model because it doesn't create a
    table in database
    It's used to declare only data schemas for the api
    """
    id: int


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
