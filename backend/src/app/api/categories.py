import uuid

from fastapi import APIRouter, Depends

from app.db.session import SessionLocal
from app.models.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.categories import CategoriesService

router = APIRouter(prefix="/categories", tags=["categories"])


def get_categories_service() -> CategoriesService:
    return CategoriesService(session=SessionLocal())


CategoriesServiceDep = Depends(get_categories_service)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(service: CategoriesService = CategoriesServiceDep):
    return service.list_categories()


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(body: CategoryCreate, service: CategoriesService = CategoriesServiceDep):
    return service.create_category(body)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: uuid.UUID, service: CategoriesService = CategoriesServiceDep
):
    return service.get_category(category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: uuid.UUID,
    body: CategoryUpdate,
    service: CategoriesService = CategoriesServiceDep,
):
    return service.update_category(category_id, body)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: uuid.UUID, service: CategoriesService = CategoriesServiceDep
):
    service.delete_category(category_id)
