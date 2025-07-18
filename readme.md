# 🛍️ Rothenberg Sports

**Tienda online de camisetas deportivas**
*Django + MariaDB + API externa + Docker*

---

## 👕 ¿Qué hace este proyecto?

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

5. Configura la base de datos MaríaDB (XAMPP):

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

Se incluye un **Dockerfile** y un volumen Docker para persistir datos en `./data/`.

1. Construye la imagen Docker:

   ```bash
   docker build -t rothenberg-sports .
   ```

2. Crea la carpeta local para la base de datos y añade al `.gitignore`:

   ```bash
   mkdir -p data
   ```

3. Ejecuta el contenedor, montando `data/`:

   ```bash
   docker run -d \
     --name rothenberg-sports \
     -p 8000:8000 \
     -v "${PWD}/data:/app/data" \
     -e USE_SQLITE=True \
     rothenberg-sports
   ```

   > **Nota:** la variable de entorno `USE_SQLITE=True` fuerza el uso de SQLite en lugar de MariaDB.

4. Dentro del contenedor, ejecuta migraciones (esto creará `db.sqlite3` en `data/`):

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

> **Nota:** El archivo `data/db.sqlite3` se generará en tu carpeta local `data/`.

---

## 🐬 Uso con Docker Compose

También puedes usar **Docker Compose** para simplificar comandos:

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
├── readme.md                # Documentación del proyecto
└── requirements.txt         # Dependencias Python
```

---

## ❓ Gitignore y base de datos

Se recomienda ignorar el archivo SQLite para no subir datos de desarrollo:

```gitignore
# SQLite
/data/db.sqlite3
```

La carpeta `data/` permanece, pero el `.sqlite3` dentro queda excluido.

---

## 🎉 ¡Listo para usar!

Elige el método (manual o Docker) y ¡disfruta tu tienda de camisetas deportivas!
