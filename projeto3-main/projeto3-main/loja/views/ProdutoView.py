from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage
from ..models import Produto, Categoria, Fabricante
import os
from django.conf import settings


def list_produto_view(request, id=None):
    # Inicia a consulta
    qs = Produto.objects.all()

    # Captura parâmetros GET
    produto_param = request.GET.get('produto')
    promocao_param = request.GET.get('promocao')
    destaque_param = request.GET.get('destaque')
    categoria_param = request.GET.get('categoria')
    fabricante_param = request.GET.get('fabricante')

    if produto_param:
        qs = qs.filter(produto__icontains=produto_param)
    if promocao_param and promocao_param.lower() in ['1', 'true', 'yes']:
        qs = qs.filter(promocao=True)
    if destaque_param and destaque_param.lower() in ['1', 'true', 'yes']:
        qs = qs.filter(destaque=True)
    if categoria_param:
        qs = qs.filter(categoria__categoria__iexact=categoria_param)
    if fabricante_param:
        qs = qs.filter(fabricante__fabricante__iexact=fabricante_param)
    if id:
        qs = qs.filter(id=id)

    print('Consulta produtos:', list(qs.values('id', 'produto')))

    context = {
        'produtos': qs,
    }
    return render(request, 'loja/produto.html', context)


def create_produto_view(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        fabricantes = Fabricante.objects.all()
        return render(request, 'loja/produto-create.html', {'categorias': categorias, 'fabricantes': fabricantes})

    # POST
    nome = request.POST.get('produto')
    destaque = request.POST.get('destaque')
    promocao = request.POST.get('promocao')
    msgPromocao = request.POST.get('msgPromocao')
    preco_raw = request.POST.get('preco') or '0'
    categoria_id = request.POST.get('CategoriaFk')
    fabricante_id = request.POST.get('FabricanteFk')
    image = request.FILES.get('image')

    destaque_bool = True if destaque and destaque.lower() in ['1', 'true', 'yes', 'on'] else False
    promocao_bool = True if promocao and promocao.lower() in ['1', 'true', 'yes', 'on'] else False

    preco = Decimal(preco_raw)

    produto = Produto()
    produto.produto = nome or ''
    produto.destaque = destaque_bool
    produto.promocao = promocao_bool
    produto.msgPromocao = msgPromocao or ''
    produto.preco = preco

    if categoria_id:
        produto.categoria = get_object_or_404(Categoria, pk=categoria_id)
    if fabricante_id:
        produto.fabricante = get_object_or_404(Fabricante, pk=fabricante_id)

    if image:
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        produto.imagem = filename

    produto.save()
    return redirect('produto_list')


def edit_produto_view(request, id):
    produto = get_object_or_404(Produto, pk=id)
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()
    return render(request, 'loja/produto-edit.html', {'produto': produto, 'categorias': categorias, 'fabricantes': fabricantes})


def edit_produto_postback(request, id):
    produto = get_object_or_404(Produto, pk=id)
    nome = request.POST.get('produto')
    destaque = request.POST.get('destaque')
    promocao = request.POST.get('promocao')
    msgPromocao = request.POST.get('msgPromocao')
    preco_raw = request.POST.get('preco') or '0'
    categoria_id = request.POST.get('CategoriaFk')
    fabricante_id = request.POST.get('FabricanteFk')
    image = request.FILES.get('image')

    produto.produto = nome or produto.produto
    produto.destaque = True if destaque and destaque.lower() in ['1', 'true', 'yes', 'on'] else False
    produto.promocao = True if promocao and promocao.lower() in ['1', 'true', 'yes', 'on'] else False
    produto.msgPromocao = msgPromocao or produto.msgPromocao
    produto.preco = Decimal(preco_raw)

    if categoria_id:
        produto.categoria = get_object_or_404(Categoria, pk=categoria_id)
    if fabricante_id:
        produto.fabricante = get_object_or_404(Fabricante, pk=fabricante_id)

    if image:
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        produto.imagem = filename

    produto.save()
    return redirect('produto_list')


def produto_detail_view(request, id):
    produto = get_object_or_404(Produto, pk=id)
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()
    return render(request, 'loja/produto-detail.html', {'produto': produto, 'categorias': categorias, 'fabricantes': fabricantes})


def produto_delete_view(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        # remove arquivo da imagem se existir
        if produto.imagem:
            image_path = os.path.join(settings.MEDIA_ROOT, produto.imagem.name)
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception:
                pass
        produto.delete()
        return redirect('produto_list')

    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()
    return render(request, 'loja/produto-delete.html', {'produto': produto, 'categorias': categorias, 'fabricantes': fabricantes})

