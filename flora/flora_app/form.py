from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        labels = {
            'nomeProduto': 'Nome do Produto',
            'quantidade': 'Quantidade do Produto' ,
            'preco_unitario': 'Preço' ,
            'CodBarras': 'Código de Barras',
        }