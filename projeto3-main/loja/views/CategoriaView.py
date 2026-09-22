from django.shortcuts import get_object_or_404, redirect, render

from ..models import Categoria


def list_categoria_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/categoria.html', {'categorias': categorias})


def create_categoria_view(request):
    if request.method == 'GET':
        return render(request, 'categoria/categoria-create.html')

    nome = request.POST.get('categoria', '').strip()
    if nome:
        categoria = Categoria(categoria=nome)
        categoria.save()
    return redirect('categoria_list')


def edit_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'GET':
        return render(request, 'categoria/categoria-edit.html', {'categoria': categoria})

    nome = request.POST.get('categoria', '').strip()
    if nome:
        categoria.categoria = nome
        categoria.save()
    return redirect('categoria_list')


def delete_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        categoria.delete()
    return redirect('categoria_list')
