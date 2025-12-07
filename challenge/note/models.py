from django.db import models as mdl
import uuid


class Note(mdl.Model):
    id = mdl.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = mdl.CharField(blank=True)
