from django.urls import path
from .views import TodoListeCreate, TodoRetieveUpdateDestroy

urlpatterns = [
    path('todos/', TodoListeCreate.as_view(), name='todos'),
    path('todos/<int:pk>/', TodoRetieveUpdateDestroy.as_view(), name='todos_d'),
]