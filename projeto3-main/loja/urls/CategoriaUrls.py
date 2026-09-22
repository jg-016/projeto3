from django.urls import path
from ..views import (
    list_categoria_view,
    create_categoria_view,
    edit_categoria_view,
    delete_categoria_view,
)

urlpatterns = [
    path('categoria/', list_categoria_view, name='categoria_list'),
    path('categoria/create/', create_categoria_view, name='categoria_create'),
    path('categoria/<int:id>/edit/', edit_categoria_view, name='categoria_edit'),
    path('categoria/<int:id>/delete/', delete_categoria_view, name='categoria_delete'),
]
