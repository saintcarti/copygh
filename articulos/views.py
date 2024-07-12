from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .models import Producto, Marca, Boleta,DetalleBoleta
from .forms import  ProductoForm
from django.contrib.auth.decorators import login_required
from .carrito import Carrito
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone


# Create your views here.

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url=login_url)

def crear(request):
    return render(request,'crud/crear.html')

def producto_detalle(request, id):
    producto = get_object_or_404(Producto, productoId=id)
    context = {
        'productos': [producto]
    }
    return render(request, 'crud/detalle.html', context)

# CRUD para producto 

@admin_required()
def producto_lista(request):
    productos = Producto.objects.all()
    context={

        'productos':productos
    }
    return render(request, 'crud/Lista_productos.html',context)


def producto_nuevo(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crud/crear.html', {'form': form})
    
def producto_editar(request, id):
    producto = get_object_or_404(Producto, productoId=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página principal o lista de productos
    else:
        form = ProductoForm(instance=producto)

    context = {
        'form': form
    }
    return render(request, 'crud/modificar.html', context)



def producto_borrar(request, pk):
    producto = get_object_or_404(Producto, productoId=pk)
    producto.delete()
    return redirect('Inicio') 

@login_required
def tienda(request):
    producto = Producto.objects.all()
    return render(request, 'vista_usuario/tienda.html', {'productos': producto})


def agregar_producto(request, id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, pk=id)
    carrito.agregar(producto=producto)
    return redirect('carrito')

def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, productoId=producto_id)
    carrito = Carrito(request)
    carrito.eliminar(producto)
    return redirect('carrito')

def restar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, productoId=producto_id)
    carrito = Carrito(request)
    carrito.restar(producto)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('carrito')


def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'vista_usuario/tienda.html', {'productos': Producto.objects.all()})  # Asegura que se renderice toda la tienda con el carrito


def generarBoleta(request):
    carrito = Carrito(request)
    if not carrito.carrito:
        return redirect('vista_usuario/tienda.html')  # Si el carrito está vacío, redirige a la tienda

    total_boleta = 0
    for item in carrito.carrito.values():
        total_boleta += float(item['precio']) * item['cantidad']

    boleta = Boleta(fecha=timezone.now(), total=total_boleta)
    boleta.save()

    productos = []
    for item in carrito.carrito.values():
        if 'producto_id' not in item:
            return redirect('vista_usuario/tienda.html')  # Maneja el caso de error, por ejemplo, redirigiendo a la tienda

        producto_id = item['producto_id']
        producto = Producto.objects.get(id=producto_id)
        cantidad = item['cantidad']
        precio = item['precio']
        subtotal = cantidad * float(precio)

        detalle_boleta = DetalleBoleta(
            boleta=boleta,
            producto=producto,
            cantidad=cantidad,
            precio=precio
        )
        detalle_boleta.save()
        productos.append(detalle_boleta)

    carrito.limpiar()  # Limpia el carrito después de generar la boleta

    datos = {
        'productos': productos,
        'fecha': boleta.fecha,
        'total': boleta.total
    }
    return render(request, 'carrito/detallecarrito.html', datos)  # Redirige a la tienda después de generar la boleta









