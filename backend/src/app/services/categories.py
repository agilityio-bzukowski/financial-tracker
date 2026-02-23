import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.db.schema import Category
from app.models.category import CategoryCreate, CategoryUpdate
from app.services.base import BaseService


class CategoriesService(BaseService):
    def list_categories(self) -> list[Category]:
        return (
            self.session.query(Category)
            .filter(Category.deleted_at.is_(None))
            .order_by(Category.sort_order)
            .all()
        )

    def get_category(self, category_id: uuid.UUID) -> Category:
        category = (
            self.session.query(Category)
            .filter(Category.id == category_id, Category.deleted_at.is_(None))
            .first()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def create_category(self, body: CategoryCreate) -> Category:
        category = Category(**body.model_dump())
        self.session.add(category)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="A category with this name and type already exists",
            )
        self.session.refresh(category)
        return category

    def update_category(self, category_id: uuid.UUID, body: CategoryUpdate) -> Category:
        category = self.get_category(category_id)
        updates = body.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(category, field, value)
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete_category(self, category_id: uuid.UUID) -> None:
        category = self.get_category(category_id)
        category.deleted_at = datetime.now(timezone.utc)
        self.session.commit()
