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
]
