from sqlalchemy.orm import  Session
from app.schema.db import Task
from typing import AnyStr, Optional
from datetime import datetime

def create_task(session: Session, description: AnyStr, finish_date: datetime, category_id:int, user_id:int) -> Task:
    create_date = datetime.now()
    # Create the task
    task = Task(description=description, create_date=create_date, finish_date=finish_date, status='pending', category_id=category_id, user_id=user_id)
    session.add(task)
    # Commit the changes
    session.commit()
    return task

def update_task(session: Session, task_id: int, description: Optional[AnyStr]= None, 
                finish_date: Optional[datetime]= None, status: Optional[AnyStr]= None) -> Task:
    # Update the task
    task = session.query(Task).filter(Task.id == task_id).first()
    if description:
        task.description = description
    if finish_date:
        task.finish_date = finish_date
    if status:
        task.status = status
    # Commit the changes
    session.commit()
    return task

def delete_task(session: Session, task_id: int) -> Task:
    # Delete the task
    task = session.query(Task).filter(Task.id == task_id).first()
    session.delete(task)
    # Commit the changes
    session.commit()
    return task

def get_task_by_user(session: Session, user_id: int) -> list[Task]:
    # Get the task list
    task_list = session.query(Task).filter(Task.user_id == user_id).all()
    return task_list

def get_task_by_id(session: Session, task_id: int) -> Task:
    # Get the task
    task = session.query(Task).filter(Task.id == task_id).first()
    return task
    