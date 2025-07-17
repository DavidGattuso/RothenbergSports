# views.py  – Pedidos / pagos con estados canónicos
from datetime import date, timedelta
import tempfile, requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .forms   import ProcesoPagoForm
from .models  import Pedido, PedidoItem, DireccionEnvio, Pago
from .utils.pdf_utils import generate_pdf_sync
from ecommerce_camisetas.models import Carrito

# ───────────── config API externa ─────────────
API_BASE   = "https://api-camisetas-c3cq.onrender.com/pedidos"

# Estados EXACTOS que entiende la API
EST_PREP   = "Preparando Pedido"
EST_TRANSP = "Entregado a Transportista"
EST_CAMINO = "En Camino a tu Dirección"
EST_FIN    = "Producto Entregado"

# ──────────────────────────────────────────────
@login_required
def proceso_pago(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form = ProcesoPagoForm(request.POST)

        if "terminos" not in request.POST:
            messages.error(request, "Debes aceptar los términos y condiciones.")
        elif form.is_valid():
            # ... (creación de dirección, pedido, ítems, pago) ...

            # alta en micro-servicio (sin headers)
            try:
                requests.post(
                    API_BASE,
                    json={
                        "id"            : pedido.id,
                        "estado"        : EST_PREP,
                        "cliente_email" : dir_env.email,
                        "codigo_entrega": None,
                    },
                    timeout=5   # ← headers eliminado
                ).raise_for_status()
            except Exception as e:
                print("API Pedidos:", e)
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

    return render(
        request,
        "proceso_pago.html",
        {
            "form"         : form,
            "total"        : carrito.total + 3990,
            "fecha_entrega": (date.today() + timedelta(days=3)).strftime("%d/%m/%Y"),
        },
    )

# ──────────────────────────────────────────────
@login_required
def detalles_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items  = pedido.items.all()
    pago   = Pago.objects.filter(pedido=pedido).first()

    # refrescar estado desde la API
    try:
        r = requests.get(f"{API_BASE}/{pedido.id}", timeout=5)  # ← headers eliminado
        if r.status_code == 200:
            estado_api = r.json().get("estado")
            if estado_api and estado_api != pedido.estado:
                pedido.estado = estado_api
                pedido.save(update_fields=["estado"])

    except Exception as e:
        print("API Pedidos (GET):", e)

    return render(
        request,
        "detalles_pedido.html",
        {"pedido": pedido, "items": items, "pago": pago},
    )

# ──────────────────────────────────────────────
@login_required
def descargar_boleta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items  = pedido.items.all()
    pago   = Pago.objects.filter(pedido=pedido).first()

    html = render_to_string("boleta_template.html",
                            {"pedido": pedido, "items": items, "pago": pago})

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        generate_pdf_sync(html, tmp.name)
        tmp.seek(0)
        pdf = tmp.read()

    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="boleta_{pedido_id}.pdf"'
    return resp