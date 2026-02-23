from app.db.schema import Settings
from app.models.setting import SettingsUpdate
from app.services.base import BaseService


class SettingsService(BaseService):
    def get_or_create_settings(self) -> Settings:
        settings = self.session.get(Settings, "default")
        if not settings:
            settings = Settings(id="default")
            self.session.add(settings)
            self.session.commit()
            self.session.refresh(settings)
        return settings

    def update_settings(self, body: SettingsUpdate) -> Settings:
        settings = self.get_or_create_settings()
        updates = body.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(settings, field, value)
        self.session.commit()
        self.session.refresh(settings)
        return settings
