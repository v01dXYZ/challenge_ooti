from .models import Todo
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    # read only
    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "status",
            "note_id",
        ]
