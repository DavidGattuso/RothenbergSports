# 🛍️ Rothenberg Sports — Django + MariaDB + API externa

# Tienda online de camisetas deportivas

# Para qué sirve:
# - Catálogo dinámico (hombre, mujer, niños)
# - Carrito con tallas
# - Checkout simulado (NO pagos reales)
# - Boletas en PDF (Playwright + Chromium headless)
# - Registro/login de usuarios
# - Panel de administración
# - API REST de productos
# - Totalmente desacoplado: consume una API externa de camisetas

# -------- Requisitos --------
# - Python 3.9+
# - XAMPP (MariaDB corriendo)
# - virtualenv instalado globalmente (pip install virtualenv)
# - Git

# -------- Instalación rápida --------

# 1. Clona el repositorio y entra a la carpeta
git clone https://github.com/DavidGattuso/RothenbergSports.git
cd RothenbergSports
code .

# 2. Crea y activa un entorno virtual (usa SIEMPRE venv como nombre de carpeta)
# Windows:
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Instala las dependencias del proyecto
pip install -r requirements.txt

# 4. Instala los navegadores de Playwright (SOLO una vez)
python -m playwright install

# Esto es obligatorio para generar los PDFs con Chromium headless.
# NO necesitas instalar WeasyPrint ni librerías nativas.

# -------- Configura la base de datos --------
# Abre XAMPP y activa MariaDB
# Ve a phpMyAdmin y crea la base de datos con nombre:
# tienda_camisetas
# (NO crees tablas: Django se encarga de todo)

# 5. Ejecuta migraciones y crea un superusuario
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Sigue los pasos: usuario, email, contraseña.

# 6. Corre el servidor
python manage.py runserver

# Abre http://127.0.0.1:8000 en tu navegador.

# -------- Funcionalidades principales --------
# - Registro e inicio de sesión de usuarios
# - Catálogo segmentado y filtrado por género/talla
# - Carrito con selección de tallas
# - Checkout simulado (sin pagos reales)
# - Descarga de boleta en PDF (HTML + imágenes externas)
# - Panel admin (/admin)
# - API REST (/api/productos/)

# -------- Crear usuarios desde el admin --------
# Entra a /admin
# Crea un usuario (Users)
# Luego crea su perfil (UserProfiles)

# ¡Listo! Ya puedes iniciar sesión y comprar.

# -------- Estructura del proyecto --------
# RothenbergSports/
# ├── app_admin/              # Administración extendida
# ├── app_pago/               # Lógica de compras y generación de boletas PDF
# │   └── utils/              # Utilidades para PDF (Playwright)
# ├── ecommerce_camisetas/    # Core de la tienda
# ├── media/                  # Imágenes locales (solo test)
# ├── static/                 # Archivos estáticos JS/CSS
# ├── tienda_camisetas/       # Proyecto principal Django
# ├── manage.py
# ├── requirements.txt
# └── .gitignore
