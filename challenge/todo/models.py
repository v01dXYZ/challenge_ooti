from django.db import models as mdl
import uuid


# Create your models here.
class Todo(mdl.Model):
    class Status(mdl.IntegerChoices):
        TODO = 0
        DONE = 1

    id = mdl.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = mdl.CharField(max_length=64)
    status = mdl.IntegerField(choices=Status)
    note_id = mdl.UUIDField(null=True)
