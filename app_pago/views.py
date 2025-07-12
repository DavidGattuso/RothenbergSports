from datetime import date, timedelta
import tempfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .forms import ProcesoPagoForm
from .models import Pedido, PedidoItem, DireccionEnvio, Pago
from .utils.pdf_utils import generate_pdf_sync
from ecommerce_camisetas.models import Carrito


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
                    producto_id_externo=item.producto_id_externo,
                    nombre=item.nombre,
                    descripcion=item.descripcion,
                    imagen_url=item.imagen_url,
                    precio=item.precio,
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

# Vista para generar y descargar la boleta en PDF con WeasyPrint
@login_required
def descargar_boleta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.all()
    pago = Pago.objects.filter(pedido=pedido).first()

    template_path = 'boleta_template.html'
    context = {
        'pedido': pedido,
        'items': items,
        'pago': pago,
    }

    # Render HTML desde template
    html_string = render_to_string(template_path, context)

    # Crear PDF temporal con Playwright
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
        generate_pdf_sync(html_string, tmp_pdf.name)
        tmp_pdf.seek(0)
        pdf_data = tmp_pdf.read()

    # Enviar respuesta PDF
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{pedido_id}.pdf"'
    return response