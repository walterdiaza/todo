from typing import AnyStr, Optional
from app.schema.db import User
from sqlalchemy.orm import  Session
from app.utils import hash_password, verify_password
from app.Oauth.oauth import oauth2_scheme, verify_token_access, create_access_token
from fastapi import Depends, HTTPException, status


def create_user(session: Session ,user_name: AnyStr, password: AnyStr, profile_picture: Optional[AnyStr] = None) -> User:
    # hash the password
    password = hash_password(password)
    print(len(password))
    # Create the user
    user = User(user_name=user_name, password=password, profile_picture=profile_picture)
    session.add(user)
    # Commit the changes
    session.commit()
    return user

def get_user(session: Session, user_name: AnyStr) -> User:
    # Get the user
    user = session.query(User).filter(User.user_name == user_name).first()
    return user

def login_user(session: Session, user_name: AnyStr, password: AnyStr) -> User:
    # Get the user
    user = session.query(User).filter(User.user_name == user_name).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user does not exist")
    # Check the password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    # Create the access token
    access_token = create_access_token(data={"user_id": user.id})

    return access_token

def get_current_user(session: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # Check if has token
    if not token:
        session.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    # Check if token is valid
    token = verify_token_access(token, credentials_exception)

    user = session.query(User).filter(User.id == token.id).first()
    if user is None:
        raise credentials_exception

    return user
