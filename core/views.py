from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .models import Cliente, Pedido, PedidoItem, Empresa, Sucursal
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

# Empresa Views
@login_required
def lista_empresas(request):
    empresas = Empresa.objects.filter(estado=True)
    return render(request, 'core/empresas/empresa_list.html', {'empresas': empresas})

@login_required
def crear_empresa(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        ruc = request.POST.get('ruc')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        
        try:
            empresa = Empresa.objects.create(
                codigo=codigo,
                nombre=nombre,
                ruc=ruc,
                direccion=direccion,
                telefono=telefono,
                email=email
            )
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('core:lista_empresas')
        except Exception as e:
            messages.error(request, f'Error al crear la empresa: {str(e)}')
    
    return render(request, 'core/empresas/empresa_form.html')

@login_required
def editar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        empresa.codigo = request.POST.get('codigo')
        empresa.nombre = request.POST.get('nombre')
        empresa.ruc = request.POST.get('ruc')
        empresa.direccion = request.POST.get('direccion')
        empresa.telefono = request.POST.get('telefono')
        empresa.email = request.POST.get('email')
        
        try:
            empresa.save()
            messages.success(request, 'Empresa actualizada exitosamente.')
            return redirect('core:lista_empresas')
        except Exception as e:
            messages.error(request, f'Error al actualizar la empresa: {str(e)}')
    
    return render(request, 'core/empresas/empresa_form.html', {'empresa': empresa})

# Sucursal Views
@login_required
def lista_sucursales(request):
    sucursales = Sucursal.objects.filter(estado=True).select_related('empresa')
    return render(request, 'core/sucursales/sucursal_list.html', {'sucursales': sucursales})

@login_required
def crear_sucursal(request):
    empresas = Empresa.objects.filter(estado=True)
    
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        
        try:
            empresa = Empresa.objects.get(id=empresa_id)
            sucursal = Sucursal.objects.create(
                empresa=empresa,
                codigo=codigo,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email=email
            )
            messages.success(request, 'Sucursal creada exitosamente.')
            return redirect('core:lista_sucursales')
        except Exception as e:
            messages.error(request, f'Error al crear la sucursal: {str(e)}')
    
    return render(request, 'core/sucursales/sucursal_form.html', {'empresas': empresas})

@login_required
def editar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    empresas = Empresa.objects.filter(estado=True)
    
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        sucursal.empresa = Empresa.objects.get(id=empresa_id)
        sucursal.codigo = request.POST.get('codigo')
        sucursal.nombre = request.POST.get('nombre')
        sucursal.direccion = request.POST.get('direccion')
        sucursal.telefono = request.POST.get('telefono')
        sucursal.email = request.POST.get('email')
        
        try:
            sucursal.save()
            messages.success(request, 'Sucursal actualizada exitosamente.')
            return redirect('core:lista_sucursales')
        except Exception as e:
            messages.error(request, f'Error al actualizar la sucursal: {str(e)}')
    
    return render(request, 'core/sucursales/sucursal_form.html', {
        'sucursal': sucursal,
        'empresas': empresas
    })
