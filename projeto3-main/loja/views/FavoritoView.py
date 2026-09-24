from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from loja.models import Favorito, Produto


@login_required
def favoritar_produto_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    favorito = Favorito.objects.filter(user=request.user, produto=produto).first()

    if not favorito:
        Favorito.objects.create(user=request.user, produto=produto)

    return redirect('/')


@login_required
def listar_favoritos_view(request):
    favoritos = Favorito.objects.filter(user=request.user).select_related('produto')

    context = {
        'favoritos': favoritos,
    }

    return render(request, 'favoritos/favoritos-listar.html', context=context)
