'''
Main file to run example API
'''
import os
from dataclasses import dataclass
import pickle

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security, UploadFile
from fastapi.security.api_key import APIKeyQuery
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session  # pylint: disable=import-error

import models  # pylint: disable=import-error
from database import SessionLocal, engine  # pylint: disable=import-error

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

_ = load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_query = APIKeyQuery(name=API_KEY_NAME)

def get_db():
    '''Get DB Session

    Yields:
        Session: DB Session
    '''
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()

async def get_api_key(api_key: str = Security(api_key_query)) -> str:
    '''Confirms API_KEY exists

    Args:
        api_key (str, optional): Name to find api. Defaults to Security(api_key_query).

    Raises:
        HTTPException: Error 403, Lack of credentials

    Returns:
        str: api key stored in .env
    '''
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=403, detail="Could not validate credentials"
    )

@dataclass
class User(BaseModel):
    '''Base model

    Args:
        "user_name": "name",
        "user_id": id,
        "user_email": "email",
        "age" (optiona): age,
        "recommendations": list[str],
        "ZIP" (optional): ZIP
    '''
    user_name: str = Field(min_length=1, max_length=16)
    user_email: str = Field(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
                            examples=['foo@bar.com'])
    age: int | None = Field(None)
    recomendations: str
    zip_code: str | None = Field(None, min_length=5, max_length=5)

@dataclass
class UserReturn(BaseModel):
    '''_summary_

    Args:
        BaseModel (_type_): _description_
    '''
    user_name: str
    user_id: int
    user_email: str
    age: int | None
    recomendations: str
    zip_code: str

@app.get("/")
def read_api(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)): # pylint: disable=unused-argument
    '''_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
        api_key (str, optional): _description_. Defaults to Depends(get_api_key).

    Returns:
        list[User]: _description_
    '''
    return db.query(models.Users).all()

@app.get("/user/{user_id}")
def find_user(user_id: int, db: Session = Depends(get_db),
              api_key: str = Depends(get_api_key)) -> UserReturn: # pylint: disable=unused-argument
    '''_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    '''
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : not found"
        )

    user = UserReturn(user_id = user_model.user_id, user_name=user_model.user_name,
                      age = user_model.age, user_email=user_model.user_email,
                      recomendations = user_model.recomendations,
                      zip_code = user_model.ZIP)
    return user

@app.post("/create")
def create_user(user: User, db: Session = Depends(get_db),
                api_key: str = Depends(get_api_key)) -> User: # pylint: disable=unused-argument
    '''_summary_

    Args:
        user (User): _description_
        ZIP (_type_, optional): _description_. Defaults to UploadFile.
        db (Session, optional): _description_. Defaults to Depends(get_db).
        api_key (str, optional): _description_. Defaults to Depends(get_api_key).

    Raises:
        HTTPException: _description_

    Returns:
        User: _description_
    '''
    user_used = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()

    if user_used is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Email {user.user_email} : Already in records"
        )

    user_model = models.Users()
    user_model.user_name = user.user_name # type: ignore
    user_model.user_email = user.user_email # type: ignore
    user_model.age = user.age # type: ignore
    user_model.recomendations = user.recomendations # type: ignore
    user_model.ZIP = user.zip_code # type: ignore

    db.add(user_model)
    db.commit()

    return user_model

@app.put("/update/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db),
                api_key: str = Depends(get_api_key)) -> User: # pylint: disable=unused-argument
    '''_summary_

    Args:
        user_id (int): _description_
        ZIP (UploadFile): _description_
        user (User): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
        api_key (str, optional): _description_. Defaults to Depends(get_api_key).

    Raises:
        HTTPException: _description_

    Returns:
        User: _description_
    '''

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    user_model.user_name = user.user_name # type: ignore
    user_model.user_email = user.user_email # type: ignore
    user_model.age = user.age # type: ignore
    user_model.recomendations = puser.recomendations # type: ignore
    user_model.ZIP = user.zip_code # type: ignore

    db.add(user_id)
    db.commit()

    return user

@app.delete("/delete/{user_id}")
def delet_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)): # pylint: disable=unused-argument
    '''_summary_

    Args:
        user_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
    '''

    book_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    db.query(models.Users).filter(models.Users.user_id == user_id).delete()

    db.commit()
