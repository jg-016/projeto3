from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=120)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.categoria
