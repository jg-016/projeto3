from django.urls import path
from ..views import (
    list_fabricante_view,
    create_fabricante_view,
    edit_fabricante_view,
    delete_fabricante_view,
)

urlpatterns = [
    path('fabricante/', list_fabricante_view, name='fabricante_list'),
    path('fabricante/create/', create_fabricante_view, name='fabricante_create'),
    path('fabricante/<int:id>/edit/', edit_fabricante_view, name='fabricante_edit'),
    path('fabricante/<int:id>/delete/', delete_fabricante_view, name='fabricante_delete'),
]
