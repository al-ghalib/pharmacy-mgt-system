from django.db import models
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  
