from sqlalchemy.orm import Session

from app.models import Category

class CategoryResolver:

    def __init__(self, db: Session):
        self.db = db

    def resolve(self, category_name: str):
        category =self.db.query(Category).filter(
            Category.name.ilike(category_name)
        ).first()
        
        return category