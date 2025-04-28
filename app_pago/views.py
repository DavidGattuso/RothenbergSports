from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.conf import settings
import os
from PIL import Image  # Importamos PIL para verificar imágenes

from .models import Pedido, PedidoItem, DireccionEnvio, Pago
from ecommerce_camisetas.models import Carrito
from .forms import ProcesoPagoForm

# Función para verificar si una imagen es válida
def is_valid_image(filepath):
    try:
        with Image.open(filepath) as img:
            img.verify()  # Intenta verificar el archivo
        return True
    except (IOError, SyntaxError) as e:
        print(f"Imagen inválida o no cargada: {filepath} - Error: {e}")
        return False

# Proceso de pago para finalizar la compra
@login_required
def proceso_pago(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = ProcesoPagoForm(request.POST)

        # Verificación de términos y formulario
        if 'terminos' not in request.POST:
            messages.error(request, 'Debes aceptar los términos y condiciones para continuar.')
        elif form.is_valid():
            direccion_envio = DireccionEnvio.objects.create(
                usuario=request.user,
                direccion=form.cleaned_data['direccion'],
                nombre=form.cleaned_data['nombre'],
                apellidos=form.cleaned_data['apellidos'],
                telefono=form.cleaned_data['telefono'],
                rut=form.cleaned_data['rut'],
                email=form.cleaned_data['email']
            )

            fecha_entrega = date.today() + timedelta(days=3)
            if fecha_entrega.weekday() == 6:
                fecha_entrega += timedelta(days=1)

            pedido = Pedido.objects.create(
                usuario=request.user,
                direccion_envio=direccion_envio,
                opciones_entrega=f"Entrega el {fecha_entrega}",
                monto_envio=3990,
                total=carrito.total + 3990,
                estado='Preparando pedido'
            )

            for item in carrito.carritoitem_set.all():
                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    talla=item.talla
                )
            carrito.carritoitem_set.all().delete()
            carrito.total = 0
            carrito.save()

            Pago.objects.create(
                usuario=request.user,
                pedido=pedido,
                metodo_pago=form.cleaned_data['metodo_pago'],
                procesado=True
            )

            messages.success(request, 'Pago realizado con éxito.')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Completa todos los campos correctamente.')
    else:
        form = ProcesoPagoForm()

    return render(request, 'proceso_pago.html', {
        'form': form,
        'total': carrito.total + 3990,
        'fecha_entrega': (date.today() + timedelta(days=3)).strftime('%d/%m/%Y')
    })

# Detalles del pedido para el usuario autenticado
@login_required
def detalles_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.all()
    pago = Pago.objects.filter(pedido=pedido).first()
    return render(request, 'detalles_pedido.html', {
        'pedido': pedido,
        'items': items,
        'pago': pago,
    })

# Vista para generar y descargar la boleta en PDF
@login_required
def descargar_boleta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.all()
    pago = Pago.objects.filter(pedido=pedido).first()

    # Asegura URLs completas para imágenes en media
    for item in items:
        if item.producto.imagen:
            imagen_path = os.path.join(settings.MEDIA_ROOT, item.producto.imagen.name)
            if is_valid_image(imagen_path):
                item.producto.imagen_url = request.build_absolute_uri(item.producto.imagen.url)
            else:
                item.producto.imagen_url = None  # Opcional: define una URL alternativa o deja en blanco

    # Contexto para la plantilla PDF
    template_path = 'boleta_template.html'
    context = {
        'pedido': pedido,
        'items': items,
        'pago': pago,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{pedido_id}.pdf"'
    template = render_to_string(template_path, context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(template.encode("UTF-8")), result, link_callback=fetch_resources)

    if not pdf.err:
        response.write(result.getvalue())
        return response
    else:
        messages.error(request, "Hubo un error al generar la boleta en PDF.")
        return redirect('detalles_pedido', pedido_id=pedido_id)

# Callback para recursos en media
def fetch_resources(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        return path
    return uri