from django.db import models
from django.core.exceptions import ValidationError
from django.db import models

class Produto(models.Model):
    nomeProduto = models.CharField(max_length=30)
    quantidade = models.PositiveIntegerField()  
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    CodBarras = models.CharField(max_length=50, unique=True)

    def clean(self):
        if self.preco_unitario < 0:
            raise ValidationError({'preco_unitario': 'O preço não pode ser negativo.'})

    def __str__(self):
        return f"{self.nomeProduto} - {self.quantidade} unid. - R$ {self.preco_unitario}"
