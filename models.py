from dataclasses import dataclass
from sqlalchemy import Column, Integer, PickleType, String
from database import Base

@dataclass
class Users(Base):
    '''Base model

    Args:
        "user_name": "name",
        "user_id": id,
        "user_email": "email",
        "age" (optiona): age,
        "recommendations": list[str],
        "ZIP" (optional): ZIP
    '''
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_email = Column(String)
    age = Column(Integer, nullable = True)
    recomendations = Column(String)
    ZIP = Column(String, nullable = True)
