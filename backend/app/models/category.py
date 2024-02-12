from sqlalchemy.orm import  Session
from app.schema.db import Category
from typing import AnyStr


def get_category(session: Session, name: AnyStr) -> Category:
    # Get the category
    category = session.query(Category).filter(Category.name == name).first()
    return category

def get_category_by_id(session: Session, id: int) -> Category:
    # Get the category
    category = session.query(Category).filter(Category.id == id).first()
    return category

def create_category(session: Session, name: AnyStr, description: AnyStr) -> Category:
    # Create the category
    category = Category(name=name, description=description)
    session.add(category)
    # Commit the changes
    session.commit()
    return category

def delete_category(session: Session, category_id: int) -> Category:
    # Delete the category
    category = session.query(Category).filter(Category.id == category_id).first()
    session.delete(category)
    # Commit the changes
    session.commit()
    return category

def get_category_list(session: Session) -> list[Category]:
    # Get the category list
    category_list = session.query(Category).all()
    return category_list
