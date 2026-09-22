from django.contrib import admin
from .models import Fabricante, Categoria, Produto, Usuario


admin.site.register(Fabricante)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Usuario)
