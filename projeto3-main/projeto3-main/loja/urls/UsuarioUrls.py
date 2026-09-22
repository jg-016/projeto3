from django.urls import path
from ..views import edit_usuario_view, list_usuario_view

urlpatterns = [
    path('usuario/', list_usuario_view, name='usuario'),
    path('usuario/<int:usuario_id>/editar/', edit_usuario_view, name='usuario_edit'),
]
