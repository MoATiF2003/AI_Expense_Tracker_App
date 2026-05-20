from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models import Category
from app.schemas.category_schema import CategoryCreate


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db


    def create_category(
        self,
        category_data: CategoryCreate
    ) -> Category:
        
        try:
            category = Category(
                name=category_data.name,
                type=category_data.type
            )
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)

            return category
        
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )
        
        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database Error"
            )

    def get_all_categories(self):
        return self.db.query(Category).all()   