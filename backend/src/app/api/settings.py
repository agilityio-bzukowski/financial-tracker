from fastapi import APIRouter, Depends

from app.db.session import SessionLocal
from app.models.setting import SettingsResponse, SettingsUpdate
from app.services.settings import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])


def get_settings_service() -> SettingsService:
    return SettingsService(session=SessionLocal())


SettingsServiceDep = Depends(get_settings_service)


@router.get("/", response_model=SettingsResponse)
def get_settings(service: SettingsService = SettingsServiceDep):
    return service.get_or_create_settings()


@router.patch("/", response_model=SettingsResponse)
def update_settings(body: SettingsUpdate, service: SettingsService = SettingsServiceDep):
    return service.update_settings(body)
