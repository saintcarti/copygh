from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseForbidden
from .models import Producto, Marca, Boleta,DetalleBoleta
from .forms import  ProductoForm
from django.contrib.auth.decorators import login_required
from .carrito import Carrito
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            return redirect('lista_productos')  # Redirige a la página principal o lista de productos
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
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 12) 
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    return render(request, 'vista_usuario/tienda.html', {'productos': productos})


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

def restar_del_carrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(productoId=id)
    carrito.restar(producto = producto)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('carrito')


def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'vista_usuario/tienda.html', {'productos': Producto.objects.all()})  # Asegura que se renderice toda la tienda con el carrito


def generarBoleta(request):
    carrito = request.session.get('carrito', None)
    if not carrito:
        # Redirigir a una página de error o mostrar un mensaje
        return render(request, 'carrito/detallecarrito.html', {'error': 'El carrito está vacío.'})

    precio_total = 0
    detalles_boleta = []

    for key, value in carrito.items():
        precio_total += int(value['precio']) * int(value['cantidad'])

    # Crear la boleta
    boleta = Boleta(total=precio_total)
    boleta.save()

    # Crear los detalles de la boleta
    for key, value in carrito.items():
        producto = Producto.objects.get(productoId=value['productoId'])
        cant = value['cantidad']
        subtotal = cant * int(value['precio'])
        detalle = DetalleBoleta(id_boleta=boleta, id_producto=producto, cantidad=cant, subtotal=subtotal)
        detalle.save()
        detalles_boleta.append(detalle)

    datos = {
        'productos': detalles_boleta,
        'fecha': boleta.fecha,
        'total': boleta.total,
        'id_boleta': boleta.id_boleta,
    }

    request.session['boleta'] = boleta.id_boleta

    # Vaciar el carrito
    carrito = Carrito(request)
    carrito.vaciar()

    return render(request, 'carrito/detallecarrito.html', datos)







