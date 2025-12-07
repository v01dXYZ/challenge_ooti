from .models import Note
from .serializers import NoteSerializer

from rest_framework import viewsets, permissions

from django.shortcuts import render


# Create your views here.
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
