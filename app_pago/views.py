# views.py  – Pedidos / pagos con estados canónicos
from datetime import date, timedelta
import tempfile, requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .forms  import ProcesoPagoForm
from .models import Pedido, PedidoItem, DireccionEnvio, Pago
from .utils.pdf_utils import generate_pdf_sync
from ecommerce_camisetas.models import Carrito

# ───────────── config API externa ─────────────
API_BASE   = "https://api-camisetas-c3cq.onrender.com/pedidos"

# Estados EXACTOS que entiende la API
EST_PREP   = "Preparando Pedido"
EST_TRANSP = "Entregado a Transportista"
EST_CAMINO = "En Camino a tu Dirección"
EST_FIN    = "Producto Entregado"


@login_required
def proceso_pago(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form = ProcesoPagoForm(request.POST)

        if "terminos" not in request.POST:
            messages.error(request, "Debes aceptar los términos y condiciones.")
        elif form.is_valid():
            # 1) CREAR dirección de envío
            dir_env = DireccionEnvio.objects.create(
                usuario   = request.user,
                nombre    = form.cleaned_data["nombre"],
                apellidos = form.cleaned_data["apellidos"],
                telefono  = form.cleaned_data["telefono"],
                direccion = form.cleaned_data["direccion"],
                rut       = form.cleaned_data["rut"],
                email     = form.cleaned_data["email"],
            )

            # 2) Calcula fecha de entrega (evita domingo)
            fecha_entrega = date.today() + timedelta(days=3)
            if fecha_entrega.weekday() == 6:
                fecha_entrega += timedelta(days=1)

            # 3) CREAR pedido local
            pedido = Pedido.objects.create(
                usuario          = request.user,
                direccion_envio  = dir_env,
                opciones_entrega = f"Entrega el {fecha_entrega}",
                monto_envio      = 3990,
                total            = carrito.total + 3990,
                estado           = EST_PREP,
            )

            # 4) CREAR ítems del carrito como PedidoItem
            for it in carrito.carritoitem_set.all():
                PedidoItem.objects.create(
                    pedido              = pedido,
                    producto_id_externo = it.producto_id_externo,
                    nombre              = it.nombre,
                    descripcion         = it.descripcion,
                    imagen_url          = it.imagen_url,
                    precio              = it.precio,
                    cantidad            = it.cantidad,
                    talla               = it.talla,
                )

            # 5) Vaciar carrito
            carrito.carritoitem_set.all().delete()
            carrito.total = 0
            carrito.save()

            # 6) Registrar Pago local
            Pago.objects.create(
                usuario     = request.user,
                pedido      = pedido,
                metodo_pago = form.cleaned_data["metodo_pago"],
                procesado   = True,
            )

            # 7) NOTIFICAR al microservicio de pedidos
            try:
                # 7.1) Preparo lista de items
                items_payload = []
                for item in pedido.items.all():
                    items_payload.append({
                        "producto_id": item.producto_id_externo,
                        "cantidad"   : item.cantidad,
                        "precio"     : float(item.precio),
                    })

                # 7.2) Armo payload inicial con pedido.id
                payload = {
                    "id"            : pedido.id,
                    "estado"        : EST_PREP,
                    "cliente_email" : dir_env.email,
                    "codigo_entrega": None,
                    "total"         : float(pedido.total + pedido.monto_envio),
                    "items"         : items_payload,
                }

                # 7.3) Intento POST
                resp = requests.post(API_BASE, json=payload, timeout=5)

                # 7.4) Si choca por UNIQUE constraint, busco el siguiente id libre
                if resp.status_code == 400 and "UNIQUE constraint failed" in resp.text:
                    candidate = payload["id"] + 1
                    while True:
                        test_url = f"{API_BASE}/{candidate}"
                        r_test = requests.get(test_url, timeout=5)
                        # si 404 → ese id está libre
                        if r_test.status_code == 404:
                            break
                        candidate += 1

                    payload["id"] = candidate
                    resp = requests.post(API_BASE, json=payload, timeout=5)

                # 7.5) Debug y validación final
                print("API → status:", resp.status_code)
                print("API → body  :", resp.text)
                resp.raise_for_status()

                # 7.6) Guardar el external_id que devolvió la API
                data = resp.json()
                pedido.external_id = data.get("id")
                pedido.save(update_fields=["external_id"])

            except Exception as e:
                print("ERROR API Pedidos:", e)
                messages.warning(
                    request,
                    "El pedido se creó localmente pero no se registró aún en el "
                    "sistema de seguimiento. Si tienes dudas, contáctanos."
                )

            messages.success(request, "Pago realizado con éxito.")
            return redirect("perfil_usuario")


        else:
            messages.error(request, "Completa todos los campos correctamente.")
    else:
        form = ProcesoPagoForm()

    # Renderizar el formulario (GET o POST inválido)
    return render(request, "proceso_pago.html", {
        "form"         : form,
        "total"        : carrito.total + 3990,
        "fecha_entrega": (date.today() + timedelta(days=3)).strftime("%d/%m/%Y"),
    })

@login_required
def detalles_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items  = pedido.items.all()
    pago   = Pago.objects.filter(pedido=pedido).first()

    # refrescar estado desde la API solo si existe external_id
    if pedido.external_id:
        try:
            r = requests.get(f"{API_BASE}/{pedido.external_id}", timeout=5)
            if r.status_code == 200:
                estado_api = r.json().get("estado")
                if estado_api and estado_api != pedido.estado:
                    pedido.estado = estado_api
                    pedido.save(update_fields=["estado"])
        except Exception as e:
            print("ERROR API Pedidos (GET):", e)

    return render(request, "detalles_pedido.html", {
        "pedido": pedido,
        "items" : items,
        "pago"  : pago,
    })


@login_required
def descargar_boleta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items  = pedido.items.all()
    pago   = Pago.objects.filter(pedido=pedido).first()

    html = render_to_string("boleta_template.html", {
        "pedido": pedido,
        "items" : items,
        "pago"  : pago,
    })

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        generate_pdf_sync(html, tmp.name)
        tmp.seek(0)
        pdf = tmp.read()

    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="boleta_{pedido_id}.pdf"'
    return resp
