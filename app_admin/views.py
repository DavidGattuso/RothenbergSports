from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages

from ecommerce_camisetas.forms import RegistrationForm
from ecommerce_camisetas.models import Producto, UserProfile
 
from django.conf import settings



# ADMIN 

# Función para verificar si el usuario es administrador
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser or u.is_staff)(view_func)

# Panel de administración
@staff_member_required
def admin_dashboard(request):
    users = User.objects.filter(is_staff=False)  # Excluir administradores
    productos = Producto.objects.all()

    return render(request, 'admin_dashboard.html', {
        'users': users,
        'productos': productos,
        'api_token': settings.SECRET_API_TOKEN,  # Pasa el token al contexto
    })


# Eliminar usuario
@admin_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)  
    user.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('admin_dashboard')


# Función para crear un nuevo usuario desde el admin
@staff_member_required
def crear_usuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            # Crear el perfil de usuario
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date']
            )
            messages.success(request, "Usuario y perfil creados exitosamente.")
            return redirect('admin_dashboard')  # Redirige al panel de administración
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistrationForm()  # Muestra un formulario vacío
    return render(request, 'crear_usuario.html', {'form': form})




# Editar usuario en el admin
@staff_member_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)
    profile = UserProfile.objects.filter(user=user).first()

    # Para indicar que estamos en la vista de administración
    is_admin = True  

    if request.method == 'POST':
        # Actualizar datos del usuario
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        if profile:
            profile.phone = request.POST.get('phone')
            profile.save()

        messages.success(request, "Datos del usuario actualizados correctamente.")
        return redirect('admin_dashboard')

    return render(request, 'editar_usuario.html', {
        'user': user,
        'profile': profile,
        'is_admin': is_admin,  
    })