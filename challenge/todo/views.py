from .models import Todo
from .serializers import TodoSerializer

from rest_framework import viewsets, permissions

from django.shortcuts import render


# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
