from django.shortcuts import get_object_or_404, redirect, render

from ..forms import FabricanteForm
from ..models import Fabricante


def list_fabricante_view(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'fabricante/fabricante.html', {'fabricantes': fabricantes})


def create_fabricante_view(request):
    if request.method == 'GET':
        form = FabricanteForm()
        return render(request, 'fabricante/fabricante-create.html', {'form': form})

    form = FabricanteForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('fabricante_list')

    return render(request, 'fabricante/fabricante-create.html', {'form': form})


def edit_fabricante_view(request, id):
    fabricante = get_object_or_404(Fabricante, pk=id)
    if request.method == 'GET':
        form = FabricanteForm(instance=fabricante)
        return render(request, 'fabricante/fabricante-edit.html', {'form': form, 'fabricante': fabricante})

    form = FabricanteForm(request.POST, instance=fabricante)
    if form.is_valid():
        form.save()
        return redirect('fabricante_list')

    return render(request, 'fabricante/fabricante-edit.html', {'form': form, 'fabricante': fabricante})


def delete_fabricante_view(request, id):
    fabricante = get_object_or_404(Fabricante, pk=id)
    if request.method == 'POST':
        fabricante.delete()
    return redirect('fabricante_list')
