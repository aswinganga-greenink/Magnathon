from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
import json

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    simulations: List["Simulation"] = Relationship(back_populates="user")

class Simulation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    habits: str = Field(description="JSON string of habits")
    result: str = Field(description="JSON string of simulation result")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="simulations")

    @property
    def habits_dict(self):
        return json.loads(self.habits)

    @property
    def result_dict(self):
        return json.loads(self.result)
