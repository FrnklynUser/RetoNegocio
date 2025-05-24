from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Articulo
from core.forms import ArticuloForm



# Create your views here.

@login_required
def lista_articulos(request):
    articulos = Articulo.objects.filter(estado=True)
    return render(request, 'productos/lista_articulos.html', {'articulos': articulos})

@login_required
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save()
            messages.success(request, 'Artículo registrado exitosamente.')
            return redirect('productos:lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'productos/crear_articulo.html', {'form': form})

@login_required
def editar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado exitosamente.')
            return redirect('productos:lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'productos/editar_articulo.html', {'form': form})
