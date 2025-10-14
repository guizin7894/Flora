from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Produto
from .form import ProdutoForm
from decimal import Decimal
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import CharField

def listar_produto(request):
    busca = request.GET.get('q', '').strip()
    produtos = Produto.objects.all()

    if busca:
        produtos = produtos.annotate(preco_text=Cast('preco_unitario', CharField())).filter(
            Q(nomeProduto__icontains=busca) |
            Q(CodBarras__icontains=busca) |
            Q(preco_text__icontains=busca)
        )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(produtos.values('id', 'nomeProduto', 'CodBarras', 'quantidade', 'preco_unitario'))
        return JsonResponse({'produtos': data})

    return render(request, 'flora_app/listar.html', {'produtos': produtos})

def home(request):
    produto = Produto.objects.all()
    return render(request, "flora_app/home.html", {"produto": produto})

def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, "flora_app/detalhe.html", {"produto": produto})

def criar_produto(request):
    if request.method == "POST":
        produto_form = ProdutoForm(request.POST)  
        if produto_form.is_valid():
            produto_form.save()
            return redirect("home")
    else:
        produto_form = ProdutoForm()  

    return render(request, "flora_app/form.html", {
        "produto_form": produto_form,
    })

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id = id)
    if request.method == "POST":
        produto.delete()
        return redirect("listar_produto")
    return render(request, "flora_app/confirmar_exclusao.html", {"produto": produto})


def calcular_compra(request):
    produtos = Produto.objects.all()
    total = Decimal(0)
    valor_pago = Decimal(0)
    troco = Decimal(0)
    selecionados = []

    if request.method == 'POST':
        ids = request.POST.getlist('produtos')
        valor_pago_str = request.POST.get('valor_pago', '0')

        try:
            valor_pago = Decimal(valor_pago_str)
        except:
            valor_pago = Decimal(0)

        for pid in ids:
            produto = Produto.objects.get(id=pid)
            qtd_str = request.POST.get(f'quantidade_{pid}', '1')
            qtd = int(qtd_str)

            if produto.quantidade >= qtd:
                subtotal = produto.preco_unitario * qtd
                total += subtotal
                produto.quantidade -= qtd
                produto.save()
                selecionados.append({
                    'nome': produto.nomeProduto,
                    'preco': str(produto.preco_unitario), 
                    'quantidade': qtd,
                    'subtotal': str(subtotal),             
                })
            else:
                selecionados.append({
                    'nome': produto.nomeProduto,
                    'preco': str(produto.preco_unitario),
                    'quantidade': 0,
                    'subtotal': '0',
                    'mensagem': f'Estoque insuficiente (Disponível: {produto.quantidade})'
                })

        troco = valor_pago - total

        # 🔹 Converte todos os Decimal para string antes de salvar
        request.session['resultado_compra'] = {
            'total': str(total),
            'valor_pago': str(valor_pago),
            'troco': str(troco),
            'selecionados': selecionados,
        }

        return redirect('calcular_compra')

    # 🔹 GET: recupera resultado salvo
    resultado = request.session.pop('resultado_compra', None)
    if resultado:
        total = Decimal(resultado['total'])
        valor_pago = Decimal(resultado['valor_pago'])
        troco = Decimal(resultado['troco'])
        selecionados = resultado['selecionados']

    contexto = {
        'produtos': produtos,
        'selecionados': selecionados,
        'total': total,
        'valor_pago': valor_pago,
        'troco': troco,
    }

    return render(request, 'flora_app/calcular_compra.html', contexto)


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == "POST":
        produto_form = ProdutoForm(request.POST, instance=produto)
        if produto_form.is_valid():
            produto_form.save()
            return redirect("listar_produto")
    else:
        produto_form = ProdutoForm(instance=produto)

    return render(request, "flora_app/form.html", {
        "produto_form": produto_form,
        "editar": True,  # flag pra template saber que é edição
    })