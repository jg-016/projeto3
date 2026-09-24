from .HomeView import home_view
from .ProdutoView import (
	list_produto_view,
	create_produto_view,
	edit_produto_view,
	edit_produto_postback,
	produto_detail_view,
	produto_delete_view,
)
from .UsuarioView import edit_usuario_view, list_usuario_view
from .CategoriaView import (
	list_categoria_view,
	create_categoria_view,
	edit_categoria_view,
	delete_categoria_view,
)
from .FabricanteView import (
	list_fabricante_view,
	create_fabricante_view,
	edit_fabricante_view,
	delete_fabricante_view,
)
from .AuthView import login_view, register_view, logout_view
from .CarrinhoView import (
	create_carrinhoitem_view,
	list_carrinho_view,
	confirmar_carrinho_view,
	remover_item_view,
	adicionar_quantidade_view,
	diminuir_quantidade_view,
)
from .FavoritoView import favoritar_produto_view, listar_favoritos_view

__all__ = [
	'home_view',
	'list_produto_view',
	'create_produto_view',
	'edit_produto_view',
	'edit_produto_postback',
	'produto_detail_view',
	'produto_delete_view',
	'list_usuario_view',
	'edit_usuario_view',
	'list_categoria_view',
	'create_categoria_view',
	'edit_categoria_view',
	'delete_categoria_view',
	'list_fabricante_view',
	'create_fabricante_view',
	'edit_fabricante_view',
	'delete_fabricante_view',
	'login_view',
	'register_view',
	'logout_view',
	'create_carrinhoitem_view',
	'list_carrinho_view',
	'confirmar_carrinho_view',
	'remover_item_view',
	'adicionar_quantidade_view',
	'diminuir_quantidade_view',
	'favoritar_produto_view',
	'listar_favoritos_view',
]
