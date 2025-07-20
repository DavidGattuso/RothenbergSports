# 👕👚 Rothenberg Sports

**Tienda online de camisetas deportivas**
*Django + MariaDB + Docker + SQLite + APIs externas*

---

##  ⚽️ Características principales

* 🗂️ **Catálogo dinámico** (hombre, mujer, niños)
* 🛒 **Carrito** con selección de tallas
* 💳 **Checkout simulado** *(sin pagos reales)*
* 📄 **Boletas en PDF** (Playwright + Chromium headless)
* 👤 **Registro / Login** de usuarios
* ⚙️ **Panel de administración**
* 📡 **API REST** de productos
* 🔌 **Totalmente desacoplado**: consume una API externa de camisetas

---

* **Catálogo dinámico** (hombre, mujer, niños)
* **Carrito** con selección de tallas
* **Checkout simulado** *(sin pagos reales)*
* **Boletas en PDF** (Playwright + Chromium headless)
* **Registro / Login** de usuarios
* **Panel de administración**
* **API REST** de productos
* **Totalmente desacoplado**: consume una API externa de camisetas

---

## 🛠 Tecnologías utilizadas

* **Backend:** Django 3.2+
* **Base de datos:** MariaDB (producción) / SQLite (desarrollo)
* **Frontend:** Django Templates + Bootstrap 5
* **PDF:** Playwright + Chromium headless
* **Contenedores:** Docker / Docker Compose

---

## 💻 Instalación rápida (modo manual)

1. Clona el repositorio y accede:

   ```bash
   git clone https://github.com/DavidGattuso/RothenbergSports.git
   cd RothenbergSports
   code .
   ```

2. Crea y activa un entorno virtual (`venv`):

   * **Windows**:

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **macOS / Linux**:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

4. Instala navegadores para Playwright (solo una vez):

   ```bash
   python -m playwright install
   ```

5. Configura la base de datos MariaDB (XAMPP):

   * Inicia MariaDB desde XAMPP.
   * En phpMyAdmin, crea la base `tienda_camisetas`.

6. Ejecuta migraciones y crea un superusuario:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Levanta el servidor:

   ```bash
   python manage.py runserver
   ```

   Accede en `http://127.0.0.1:8000`

---

## 📦 Uso con Docker

1. Construye la imagen Docker:

   ```bash
   docker build -t rothenberg-sports .
   ```

2. Crea la carpeta local para la base de datos y añade al `.gitignore`:

   ```bash
   mkdir -p data
   ```

3. Ejecuta el contenedor con SQLite:

   ```bash
   docker run -d \
     --name rothenberg-sports \
     -p 8000:8000 \
     -v "${PWD}/data:/app/data" \
     -e USE_SQLITE=True \
     rothenberg-sports
   ```

4. Dentro del contenedor, ejecuta migraciones:

   ```bash
   docker exec rothenberg-sports python manage.py makemigrations
   docker exec rothenberg-sports python manage.py migrate
   ```

5. (Opcional) Crea un superusuario:

   ```bash
   docker exec -it rothenberg-sports python manage.py createsuperuser
   ```

6. Abre en el navegador:

   ```text
   http://localhost:8000
   ```

---

## 📡 Consumo de la API de Camisetas

Este proyecto obtiene las camisetas desde una API externa pública que solo permite **operaciones GET**. No es posible editar, actualizar ni borrar recursos.

* **Endpoint base:** `https://api-camisetas-c3cq.onrender.com/camisetas`
* **Operaciones disponibles:**

  * `GET /camisetas/` → Lista todas las camisetas.
  * `GET /camisetas/{id}/` → Obtiene el detalle de una camiseta por su ID.
  * Filtros por query-string: `?genero=Masculino`, `?genero=Femenino`, `?genero=Niños`, etc.

### Configuración de IDs en `views.py`

En `ecommerce_camisetas/views.py` se definen listas de IDs para categorizar las camisetas:

```python
# IDs para la pantalla principal (destacados)
CAMISETAS_INDEX_IDS = [ /* Se recomienda destacar 1 de Hombre, Mujer y Niño */ ]
# IDs de camisetas de hombre (primeras 300)
CAMISETAS_HOMBRE_IDS = [ /* 1 - 300 IDs */ ]
# IDs de camisetas de mujer (siguientes 30)
CAMISETAS_MUJER_IDS = [ /* 301 - 330 IDs */ ]
# IDs de camisetas de niños (últimas 20)
CAMISETAS_NINOS_IDS = [ /* 331 - 350 IDs */ ]
```

Así, el buscador de la aplicación podrá mostrar todas las camisetas de equipos y países de todos los continentes usando estas listas.

---

## 🚚 Consumo de la API de Pedidos

Se proporciona un **panel administrativo de logística** para cambiar el estado de los pedidos y simular el envío de correos y la validación de entregas.

1. Accede al panel:
   `https://api-camisetas-c3cq.onrender.com/static/pedidos_admin.html`
2. Introduce el **token de seguridad**: `12345` y haz clic en **Cargar Pedidos**.
3. Verás la lista de pedidos y sus estados actuales:

   * Preparando Pedido
   * Entregado a Transportista
   * En Camino a tu Dirección
   * Pedido Entregado
4. Para simular el envío de un **código de entrega** al cliente (integración con Mailjet):

   * Selecciona un pedido.
   * Cambia su estado a **En Camino a tu Dirección**.
   * Al guardar, el sistema generará un **código único** y enviará un correo al email que indiques mediante Mailjet (simulación).
   * Copia el código recibido.
5. Validación del código por el cliente:

   * El cliente debe introducir el código en el mismo panel o en la interfaz correspondiente.
   * Si el código coincide, el pedido cambiará a **Pedido Entregado**.
   * Se mostrará en la página que el producto ya está entregado.

---

## ⚙️ Disponibilidad de las APIs

Las **APIs de Camisetas** y de **Pedidos** están desplegadas en Render (plan gratuito). Render hiberna las aplicaciones tras periodos de inactividad, por lo que podría haber demoras iniciales al acceder:

* Para mitigarlo, se configuró **Uptime Robot** para enviar un ping cada 5 minutos, manteniendo las APIs activas durante más tiempo.
* Aun así, no hay garantía de disponibilidad continua; si la API está durmiendo, puede tardar hasta 2 minutos en responder.

---

## 🐬 Uso con Docker Compose

* Levanta servicios:

  ```bash
  docker-compose up --build -d
  ```
* Detén y elimina contenedores:

  ```bash
  docker-compose down
  ```

---

## 📁 Estructura del proyecto

```text
RothenbergSports/
├── app_admin/               # Administración extendida
├── app_pago/                # Lógica de compras y generación de boletas PDF
├── data/                    # Base para la base de datos SQLite (montaje Docker)
├── ecommerce_camisetas/     # Core de la tienda
├── media/                   # Imágenes locales (solo pruebas)
├── static/                  # Archivos estáticos (JS/CSS)
├── tienda_camisetas/        # Proyecto principal Django
├── venv/                    # Entorno virtual (opcional manual)
├── .dockerignore            # Ignorar archivos para Docker
├── .gitignore               # Ignorar archivos locales
├── docker-compose.yml       # Configuración Docker Compose
├── Dockerfile               # Imagen Docker
├── manage.py                # Script de gestión Django
├── README.md                # Documentación del proyecto
└── requirements.txt         # Dependencias Python
```

---

## 🎉 ¡Listo para usar!

Elige el método (manual o Docker) y ¡disfruta de las camisetas deportivas de Rothenberg Sports!
