from django.urls import path

from loja.views.FavoritoView import favoritar_produto_view, listar_favoritos_view

urlpatterns = [
    path('', listar_favoritos_view, name='listar_favoritos'),
    path('<int:produto_id>/', favoritar_produto_view, name='favoritar_produto'),
]
