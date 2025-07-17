from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import requests
from .models import Producto, Carrito, CarritoItem, UserProfile
from .forms import UserProfileUpdateForm, RegistrationForm
from app_pago.models import Pedido  

API_URL = "https://api-camisetas-c3cq.onrender.com/camisetas"

CAMISETAS_INDEX_IDS = [229, 318, 340]
CAMISETAS_HOMBRE_IDS = [229, 183, 218, 185, 224, 209, 28, 41, 92, 81, 269, 290, 114, 125, 123, 131, 152, 168, 16, 48, 94]
CAMISETAS_MUJER_IDS = [305, 318, 320, 316, 323, 326, 325, 312, 330, 315, 308, 314]
CAMISETAS_NINOS_IDS = [335, 333, 334, 340, 350, 345, 343, 339, 336]

def index(request):
    camisetas_index = []
    for id_ in CAMISETAS_INDEX_IDS:
        resp = requests.get(f"{API_URL}/{id_}")
        if resp.status_code == 200:
            producto = resp.json()
            producto["imagen_url"] = producto.get("imagen", "")
            producto["precio_redondeado"] = round(producto.get("valor", 0))
            camisetas_index.append(producto)
    return render(request, 'index.html', {
        'camisetas_index': camisetas_index,
    })

def hombre_index(request):
    productos_hombre = []
    for id_ in CAMISETAS_HOMBRE_IDS:
        resp = requests.get(f"{API_URL}/{id_}")
        if resp.status_code == 200:
            producto = resp.json()
            producto["imagen_url"] = producto.get("imagen", "")
            producto["precio_redondeado"] = round(producto.get("valor", 0))
            productos_hombre.append(producto)
    return render(request, "hombre_index.html", {"productos_hombre": productos_hombre})

def mujer_index(request):
    productos_mujer = []
    for id_ in CAMISETAS_MUJER_IDS:
        resp = requests.get(f"{API_URL}/{id_}")
        if resp.status_code == 200:
            producto = resp.json()
            producto["imagen_url"] = producto.get("imagen", "")
            producto["precio_redondeado"] = round(producto.get("valor", 0))
            productos_mujer.append(producto)
    return render(request, "mujer_index.html", {"productos_mujer": productos_mujer})

def ninos_index(request):
    productos_ninos = []
    for id_ in CAMISETAS_NINOS_IDS:
        resp = requests.get(f"{API_URL}/{id_}")
        if resp.status_code == 200:
            producto = resp.json()
            producto["imagen_url"] = producto.get("imagen", "")
            producto["precio_redondeado"] = round(producto.get("valor", 0))
            productos_ninos.append(producto)
    return render(request, "ninos_index.html", {"productos_ninos": productos_ninos})

def detalle_producto(request, producto_id):
    producto_id = int(producto_id)
    origen = request.GET.get("origen", "index")
    if origen == "hombre":
        id_list = CAMISETAS_HOMBRE_IDS
    elif origen == "mujer":
        id_list = CAMISETAS_MUJER_IDS
    elif origen == "ninos":
        id_list = CAMISETAS_NINOS_IDS
    else:
        id_list = CAMISETAS_INDEX_IDS

    resp = requests.get(f"{API_URL}/{producto_id}")
    if resp.status_code != 200:
        from django.http import Http404
        raise Http404("Producto no encontrado")
    producto = resp.json()
    producto["imagen_url"] = producto.get("imagen", "")
    producto["precio_redondeado"] = round(producto.get("valor", 0))

    try:
        idx = id_list.index(producto_id)
    except ValueError:
        idx = -1

    producto_anterior = None
    producto_siguiente = None
    if idx != -1:
        if idx > 0:
            pid = id_list[idx - 1]
            r_ant = requests.get(f"{API_URL}/{pid}")
            if r_ant.status_code == 200:
                producto_anterior = r_ant.json()
        if idx < len(id_list) - 1:
            pid = id_list[idx + 1]
            r_sig = requests.get(f"{API_URL}/{pid}")
            if r_sig.status_code == 200:
                producto_siguiente = r_sig.json()

    tallas_disponibles = [
        {"talla": "S", "get_talla_display": "S"},
        {"talla": "M", "get_talla_display": "M"},
        {"talla": "L", "get_talla_display": "L"},
        {"talla": "XL", "get_talla_display": "XL"},
    ]

    return render(request, 'producto_detalle.html', {
        'producto': producto,
        'tallas_disponibles': tallas_disponibles,
        'producto_anterior': producto_anterior,
        'producto_siguiente': producto_siguiente,
        'origen': origen, 
    })

def buscar(request):
    query = request.GET.get('q', '').strip()
    productos_hombre, productos_mujer, productos_ninos = [], [], []

    if query:
        url_hombre = f"{API_URL}?genero=Masculino&nombre={query}"
        url_mujer  = f"{API_URL}?genero=Femenino&nombre={query}"
        url_ninos  = f"{API_URL}?genero=Niños&nombre={query}"

        resp = requests.get(url_hombre)
        if resp.status_code == 200:
            productos_hombre = resp.json()
            for p in productos_hombre:
                p["imagen_url"] = p.get("imagen", "")
                p["precio_redondeado"] = round(p.get("valor", 0))

        resp = requests.get(url_mujer)
        if resp.status_code == 200:
            productos_mujer = resp.json()
            for p in productos_mujer:
                p["imagen_url"] = p.get("imagen", "")
                p["precio_redondeado"] = round(p.get("valor", 0))

        resp = requests.get(url_ninos)
        if resp.status_code == 200:
            productos_ninos = resp.json()
            for p in productos_ninos:
                p["imagen_url"] = p.get("imagen", "")
                p["precio_redondeado"] = round(p.get("valor", 0))

    def eliminar_duplicados(lista):
        vistos = set()
        resultado = []
        for p in lista:
            if p["id"] not in vistos:
                resultado.append(p)
                vistos.add(p["id"])
        return resultado

    productos_hombre = eliminar_duplicados(productos_hombre)
    productos_mujer = eliminar_duplicados(productos_mujer)
    productos_ninos = eliminar_duplicados(productos_ninos)

    return render(request, 'resultados_busqueda.html', {
        'productos_hombre': productos_hombre,
        'productos_mujer': productos_mujer,
        'productos_ninos': productos_ninos,
        'query': query
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
        messages.error(request, 'No se encontró el perfil. Completa tu información.')
        return redirect('crear_perfil')

    pedidos = Pedido.objects.filter(usuario=request.user)

    # 🔵 refresca cada estado contra la API plural
    for p in pedidos:
        try:
            r = requests.get(f"https://api-camisetas-c3cq.onrender.com/pedidos/{p.id}", timeout=5)
            if r.status_code == 200:
                p.estado = r.json().get("estado", p.estado)
        except Exception as e:
            print(f"API Pedidos (perfil) {p.id}: {e}")

    return render(request, "perfil.html", {"profile": profile, "pedidos": pedidos})



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
    talla_seleccionada = request.POST.get('talla')
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    try:
        response = requests.get(f"{API_URL}/{producto_id}/")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        messages.error(request, "No se pudo obtener el producto desde la API.")
        return redirect('ver_carrito')

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto_id_externo=producto_id,
        talla=talla_seleccionada,
        defaults={
            'nombre': data['nombre'],
            'descripcion': data.get('descripcion', ''),
            'imagen_url': data['imagen'],
            'precio': data['valor'],
            'cantidad': 1,
        }
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