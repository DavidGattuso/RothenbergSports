from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from ecommerce_camisetas.forms import RegistrationForm
from ecommerce_camisetas.models import UserProfile

# Función para verificar si el usuario es administrador
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser or u.is_staff)(view_func)

# Panel de administración SOLO usuarios
@staff_member_required
def admin_dashboard(request):
    users = User.objects.filter(is_staff=False)  # Excluir administradores
    return render(request, 'admin_dashboard.html', {
        'users': users
    })

# Eliminar usuario
@admin_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)
    user.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('admin_dashboard')

# Crear usuario
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
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistrationForm()
    return render(request, 'crear_usuario.html', {'form': form})

# Editar usuario
@staff_member_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)
    profile = UserProfile.objects.filter(user=user).first()
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
        'is_admin': True,  # Opcional, por si lo usas en template
    })
