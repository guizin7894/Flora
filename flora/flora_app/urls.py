from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("criar/", views.criar_produto, name="criar_produto"),
    path("listar/", views.listar_produto, name="listar_produto"),
    path("produto/<int:id>/editar/", views.editar_produto, name="editar_produto"),  
    path("produto/<int:id>/excluir/", views.excluir_produto, name="excluir_produto"),
    path("produto/<int:id>/", views.detalhe_produto, name="detalhe_produto"),
    path("compra/", views.calcular_compra, name="calcular_compra"),
]