from django.urls import path

from loja.views.CarrinhoView import (
    adicionar_quantidade_view,
    confirmar_carrinho_view,
    create_carrinhoitem_view,
    diminuir_quantidade_view,
    list_carrinho_view,
    remover_item_view,
)

urlpatterns = [
    path('', list_carrinho_view, name='list_carrinho'),
    path('<int:produto_id>', create_carrinhoitem_view, name='create_carrinhoitem'),
    path('confirmar', confirmar_carrinho_view, name='confirmar_carrinho'),
    path('remover/<int:item_id>/', remover_item_view, name='remover_carrinhoitem'),
    path('adicionar/<int:item_id>/', adicionar_quantidade_view, name='adicionar_quantidade'),
    path('diminuir/<int:item_id>/', diminuir_quantidade_view, name='diminuir_quantidade'),
]