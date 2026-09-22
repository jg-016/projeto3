from django.db import models
from .Categoria import Categoria
from .Fabricante import Fabricante


class Produto(models.Model):
    produto = models.CharField(max_length=200)
    destaque = models.BooleanField(default=False)
    promocao = models.BooleanField(default=False)
    msgPromocao = models.CharField(max_length=200, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.produto
