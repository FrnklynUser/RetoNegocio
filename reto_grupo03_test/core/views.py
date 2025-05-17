from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .models import Cliente, Pedido, PedidoItem
from productos.models import Articulo
from promociones.models import Promocion
from .forms import ClienteForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:login')

@login_required
def dashboard(request):
    promociones = Promocion.objects.filter(
        estado=True,
        fecha_inicio__lte=timezone.now(),
        fecha_fin__gte=timezone.now()
    ).select_related(
        'empresa', 'sucursal', 'canal_cliente'
    ).prefetch_related('articulos')
    
    context = {
        'promociones': promociones
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        items = request.POST.getlist('items[]')
        cantidades = request.POST.getlist('cantidades[]')
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            pedido = Pedido.objects.create(
                cliente=cliente,
                fecha=timezone.now(),
                monto_total=0
            )
            
            monto_total = 0
            for item, cantidad in zip(items, cantidades):
                articulo = Articulo.objects.get(id=item)
                cantidad = int(cantidad)
                subtotal = articulo.precio * cantidad
                monto_total += subtotal
                
                PedidoItem.objects.create(
                    pedido=pedido,
                    articulo=articulo,
                    cantidad=cantidad,
                    precio_unitario=articulo.precio,
                    subtotal=subtotal
                )
            
            pedido.monto_total = monto_total
            pedido.save()
            
            # Procesar promociones
            bonificaciones = procesar_promociones(pedido)
            
            messages.success(request, 'Pedido creado exitosamente')
            return redirect('core:detalle_pedido', pedido_id=pedido.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear el pedido: {str(e)}')
            return redirect('core:crear_pedido')
    
    clientes = Cliente.objects.filter(estado=True)
    articulos = Articulo.objects.filter(estado=True)
    
    context = {
        'clientes': clientes,
        'articulos': articulos
    }
    return render(request, 'core/crear_pedido.html', context)

@login_required
def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    items = PedidoItem.objects.filter(pedido=pedido)
    bonificaciones = procesar_promociones(pedido)
    
    context = {
        'pedido': pedido,
        'items': items,
        'bonificaciones': bonificaciones
    }
    return render(request, 'core/detalle_pedido.html', context)

def procesar_promociones(pedido):
    """
    Procesa las promociones aplicables a un pedido y retorna las bonificaciones correspondientes
    """
    from promociones.services import PromocionService
    
    # Preparar los items del pedido para el servicio
    items = [
        {
            'articulo_id': item.articulo_id,
            'cantidad': item.cantidad,
            'precio': item.precio_unitario
        }
        for item in pedido.pedidoitem_set.all()
    ]
    
    # Obtener bonificaciones del servicio
    bonificaciones = PromocionService.calcular_bonificaciones(
        canal_cliente_id=pedido.cliente.canal_id,
        items=items
    )
    
    # Convertir IDs de artículos a objetos
    articulos_dict = {
        art.id: art 
        for art in Articulo.objects.filter(
            id__in=[b['articulo_id'] for b in bonificaciones]
        )
    }
    
    # Formatear bonificaciones para la vista
    return [
        {
            'articulo': articulos_dict[b['articulo_id']],
            'cantidad': b['cantidad'],
            'tipo': 'Bonificación'
        }
        for b in bonificaciones
    ]

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'core/clientes/lista_clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('core:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'core/clientes/crear_cliente.html', {'form': form})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('core:lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/clientes/editar_cliente.html', {'form': form})
