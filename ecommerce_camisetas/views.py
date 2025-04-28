from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Producto, Carrito, CarritoItem, UserProfile
from .forms import UserProfileUpdateForm, RegistrationForm
from app_pago.models import Pedido  # Importación del modelo Pedido desde app_pago


# Página principal con productos categorizados
def index(request):
    productos_hombre = Producto.objects.filter(categoria__nombre='Hombre')
    productos_mujer = Producto.objects.filter(categoria__nombre='Mujer')
    productos_ninos = Producto.objects.filter(categoria__nombre='Niños')
    return render(request, 'index.html', {
        'productos_hombre': productos_hombre,
        'productos_mujer': productos_mujer,
        'productos_ninos': productos_ninos,
    })


# Vistas de productos por categoría
def hombre_view(request):
    productos_hombre = Producto.objects.filter(categoria__nombre='Hombre')
    return render(request, 'hombre_index.html', {'productos_hombre': productos_hombre})

def mujer_view(request):
    productos_mujer = Producto.objects.filter(categoria__nombre='Mujer')
    return render(request, 'mujer_index.html', {'productos_mujer': productos_mujer})

def ninos_view(request):
    productos_ninos = Producto.objects.filter(categoria__nombre='Niños')
    return render(request, 'ninos_index.html', {'productos_ninos': productos_ninos})


# Detalle de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    tallas_disponibles = producto.tallas_disponibles.all()

    # Obtener todos los productos de la misma categoría
    categoria_actual = producto.categoria
    productos_categoria = Producto.objects.filter(categoria=categoria_actual).order_by('id')

    # Encontrar el índice del producto actual
    indice_producto_actual = list(productos_categoria).index(producto)

    # Determinar el producto anterior y siguiente
    producto_anterior = productos_categoria[indice_producto_actual - 1] if indice_producto_actual > 0 else None
    producto_siguiente = productos_categoria[indice_producto_actual + 1] if indice_producto_actual < len(productos_categoria) - 1 else None

    return render(request, 'producto_detalle.html', {
        'producto': producto,
        'tallas_disponibles': tallas_disponibles,
        'producto_anterior': producto_anterior,
        'producto_siguiente': producto_siguiente,
    })


# Vista para buscar productos por nombre
def buscar(request):
    query = request.GET.get('q')
    productos_hombre = productos_mujer = productos_ninos = None

    if query:
        productos_hombre = Producto.objects.filter(nombre__icontains=query, categoria__nombre='Hombre')
        productos_mujer = Producto.objects.filter(nombre__icontains=query, categoria__nombre='Mujer')
        productos_ninos = Producto.objects.filter(nombre__icontains=query, categoria__nombre='Niños')

    return render(request, 'resultados_busqueda.html', {
        'productos_hombre': productos_hombre,
        'productos_mujer': productos_mujer,
        'productos_ninos': productos_ninos,
    })


# Registro de usuarios
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date']
            )
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})






# Manejo de login de usuario
def login_view(request):
    next_url = request.GET.get('next', 'index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            
            # Redirigir según el tipo de usuario
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')  # Ruta para el panel de administración
            return redirect(next_url)  # Ruta normal para usuarios
        messages.error(request, 'Correo o contraseña incorrectos.')
    return render(request, 'login.html')



# Vista de perfil de usuario con historial de pedidos
@login_required
def perfil_usuario(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if not profile:
        messages.error(request, 'No se encontró el perfil. Por favor, complete su información.')
        return redirect('crear_perfil')
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'perfil.html', {'profile': profile, 'pedidos': pedidos})


# Vista de logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('index')  # Redirige a la página principal


# Actualizar perfil del usuario
@login_required
def actualizar_perfil(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Guarda los datos de User
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            
            # Guarda el perfil
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Error al actualizar el perfil.')
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, 'actualizar_perfil.html', {
        'form': form,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    })


# Eliminar cuenta del usuario
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Cuenta eliminada exitosamente.')
        return redirect('index')
    return render(request, 'confirmar_eliminar_cuenta.html')


# Funcionalidades del carrito de compras
@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'carrito.html', {'carrito': carrito})


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    talla_seleccionada = request.POST.get('talla')
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito, 
        producto=producto, 
        talla=talla_seleccionada,
        defaults={'cantidad': 1}
    )
    if not created:
        item.cantidad += 1
        item.save()
    carrito.total = sum(i.subtotal() for i in carrito.carritoitem_set.all())
    carrito.save()
    return redirect('ver_carrito')


@login_required
def incrementar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    item.cantidad += 1
    item.save()
    item.carrito.total = sum(i.subtotal() for i in item.carrito.carritoitem_set.all())
    item.carrito.save()
    return redirect('ver_carrito')


@login_required
def decrementar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    item.carrito.total = sum(i.subtotal() for i in item.carrito.carritoitem_set.all())
    item.carrito.save()
    return redirect('ver_carrito')


@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    item.delete()
    item.carrito.total = sum(i.subtotal() for i in item.carrito.carritoitem_set.all())
    item.carrito.save()
    return redirect('ver_carrito')






