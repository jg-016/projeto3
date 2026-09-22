from .HomeUrls import urlpatterns as home_urls
from .ProdutoUrls import urlpatterns as produto_urls
from .CategoriaUrls import urlpatterns as categoria_urls
from .FabricanteUrls import urlpatterns as fabricante_urls
from .UsuarioUrls import urlpatterns as usuario_urls
from .AuthUrls import urlpatterns as auth_urls

urlpatterns = []
urlpatterns += home_urls
urlpatterns += produto_urls
urlpatterns += categoria_urls
urlpatterns += fabricante_urls
urlpatterns += usuario_urls
urlpatterns += auth_urls
