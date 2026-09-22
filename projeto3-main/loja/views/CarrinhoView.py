from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from loja.models import Carrinho, CarrinhoItem, Produto


def _get_session_cart(request):
    cart_id = request.session.get('carrinho_id')
    if not cart_id:
        return None

    return Carrinho.objects.filter(id=cart_id, situacao=0).first()


@transaction.atomic
def create_carrinhoitem_view(request, produto_id=None):
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho = _get_session_cart(request)

    if carrinho is None or timezone.localdate() != timezone.localtime(carrinho.criado_em).date():
        carrinho = Carrinho.objects.create()
        request.session['carrinho_id'] = carrinho.id

    item, created = CarrinhoItem.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 1, 'preco': produto.preco},
    )
    if not created:
        item.quantidade += 1
        item.save(update_fields=['quantidade'])

    return redirect('list_carrinho')


def list_carrinho_view(request):
    carrinho = _get_session_cart(request)
    itens = carrinho.itens.select_related('produto').all() if carrinho else []

    return render(
        request,
        'carrinho/carrinho-listar.html',
        {'carrinho': carrinho, 'itens': itens},
    )


@login_required
def confirmar_carrinho_view(request):
    carrinho = _get_session_cart(request)

    if carrinho is None:
        return redirect('list_carrinho')

    carrinho.user = request.user
    carrinho.situacao = 1
    carrinho.confirmado_em = timezone.now()
    carrinho.save(update_fields=['user', 'situacao', 'confirmado_em'])

    return render(
        request,
        'carrinho/carrinho-confirmado.html',
        {'carrinho': carrinho},
    )


@require_POST
def remover_item_view(request, item_id):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    carrinho_id = request.session.get('carrinho_id')

    if str(carrinho_id) == str(item.carrinho_id):
        item.delete()

    return redirect('list_carrinho')