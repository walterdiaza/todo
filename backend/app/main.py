from fastapi import FastAPI, HTTPException, status, Depends, Header
from app.infrastructure.connectors.db import get_engine
from app.schema.pydantic import pydantic_user, pydantic_category, pydantic_create_task, pydantic_update_task
from app.schema.db import Base
from app.models.user import get_user, create_user, login_user, get_current_user
from app.models.category import get_category, create_category, delete_category, get_category_list, get_category_by_id
from sqlalchemy.orm import sessionmaker, Session
from app.models.task import create_task, update_task, delete_task, get_task_by_user, get_task_by_id

app = FastAPI()
db_engine = get_engine()
Base.metadata.create_all(db_engine)

def get_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session

# Users endpoints

@app.post("/usuarios",status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_details: pydantic_user, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = get_user(session, user_details.user_name)
    if existing_user:
        session.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    # Create the user
    create_user(session, user_details.user_name, user_details.password, user_details.profile_picture)
    session.close()
    return {"message": "User created successfully"}

@app.post("/usuarios/iniciar-sesion", status_code=status.HTTP_200_OK)
async def login_user_endpoint(user_details: pydantic_user, session: Session = Depends(get_session)):
    try:
        token = login_user(session, user_details.user_name, user_details.password)
    finally:
        session.close()

    return {"access_token": token, "token_type": "bearer"}

# Category endpoints

@app.post("/categorias", status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(category_details: pydantic_category, session: Session = Depends(get_session)):
    # Check if category already exists
    existing_category = get_category(session, category_details.name)
    if existing_category:
        session.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    # Create the category
    create_category(session, category_details.name, category_details.description)
    session.close()
    return {"message": "Category created successfully"}

@app.delete("/categorias/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category_endpoint(category_id: int, session: Session = Depends(get_session)):
    # Delete the category
    delete_category(session, category_id)
    session.close()
    return {"message": "Category deleted successfully"}

@app.get("/categorias", status_code=status.HTTP_200_OK)
async def get_category_list_endpoint(session: Session = Depends(get_session)):
    # Get the category list
    category_list = get_category_list(session)
    session.close()
    return category_list

# Tasks endpoints

@app.post("/tareas", status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task_details: pydantic_create_task, session: Session = Depends(get_session),
                                x_token: str = Header(None, convert_underscores=True)):
    # Get user from token
    user = get_current_user(session, x_token)
    user_id = user.id
    # Check if category exists
    existing_category = get_category_by_id(session, task_details.category_id)
    if not existing_category:
        session.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    # Create the task
    create_task(session, task_details.description, task_details.finish_date, task_details.category_id, user_id)
    session.close()
    return {"message": "Task created successfully"}

@app.put("/tareas/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_endpoint(task_id: int, task_details: pydantic_update_task, session: Session = Depends(get_session),
                                x_token: str = Header(None, convert_underscores=True)):
    # Get user from token
    user = get_current_user(session, x_token)
    user_id = user.id
    # Check if task exists
    existing_task = get_task_by_id(session, task_id)
    if not existing_task:
        session.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # Check if task belongs to user
    if existing_task.user_id != user_id:
        session.close()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Task does not belong to user")
    # Update the task
    task = update_task(session, task_id, task_details.description, task_details.finish_date, task_details.status)
    session.close()
    return {"message": "Task updated successfully"}

@app.delete("/tareas/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task_endpoint(task_id: int, session: Session = Depends(get_session),
                                x_token: str = Header(None, convert_underscores=True)):
    # Get user from token
    user = get_current_user(session, x_token)
    user_id = user.id
    # Check if task exists
    existing_task = get_task_by_id(session, task_id)
    if not existing_task:
        session.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # Check if task belongs to user
    if existing_task.user_id != user_id:
        session.close()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Task does not belong to user")
    # Delete the task
    delete_task(session, task_id)
    session.close()
    return {"message": "Task deleted successfully"}

@app.get("/tareas/usuario", status_code=status.HTTP_200_OK)
async def get_task_by_user_endpoint(session: Session = Depends(get_session),
                                x_token: str = Header(None, convert_underscores=True)):
    # Get user from token
    user = get_current_user(session, x_token)
    user_id = user.id
    # Get the task list
    task_list = get_task_by_user(session, user_id)
    session.close()
    return task_list

@app.get("/tareas/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id_endpoint(task_id: int, session: Session = Depends(get_session),
                                x_token: str = Header(None, convert_underscores=True)):
    # Get user from token
    user = get_current_user(session, x_token)
    user_id = user.id
    # Get the task
    task = get_task_by_id(session, task_id)
    session.close()
    return task
