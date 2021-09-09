from django.conf import settings
from django.db import models
from pathlib import Path
import uuid


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(auto_now_add=True)
    items_count = models.PositiveIntegerField(default=0)

    @property
    def filename(self):
        return f"{self.id.hex}.csv"

    @property
    def full_filename_path(self) -> Path:
        return settings.COLLECTIONS_DIR.joinpath(self.filename)

    @property
    def full_filename(self) -> Path:
        return str(self.full_filename_path)
