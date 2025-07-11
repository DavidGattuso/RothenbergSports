# 🛍️ Rothenberg Sports

Tienda online de camisetas deportivas — Django + MariaDB + API externa

## 🚀 ¿Para qué sirve esto?

Tienda web con:

- Catálogo dinámico (hombre, mujer, niños)
- Carrito con tallas
- Checkout simulado (NO hay pagos reales)
- **Boletas en PDF (Playwright + Chromium headless)**
- Registro/login de usuarios
- Panel de administración
- API REST de productos
- Totalmente desacoplado: consume una API externa de camisetas (fácil de adaptar)

## ⚙️ Requisitos

- Python 3.9+
- XAMPP (MariaDB corriendo)
- virtualenv instalado globalmente (`pip install virtualenv`)
- Git

## 💻 Instalación rápida

### 1. Clona el repositorio

git clone https://github.com/DavidGattuso/RothenbergSports.git
cd RothenbergSports
code .

### 2. Crea y activa un entorno virtual

Siempre usa venv como nombre de la carpeta virtual (no env).

Windows:

python -m venv venv
.\venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

### 3. Instala las dependencias del proyecto

pip install -r requirements.txt

### 4. Instala los navegadores de Playwright (SOLO una vez)

python -m playwright install

Esto es obligatorio para generar correctamente los PDFs con Chromium headless.

🧾 Generación de PDFs

La generación de boletas se realiza con Playwright + Chromium headless, compatible con:

HTML dinámico generado desde Django

Imágenes remotas desde la API externa

CSS moderno

✅ No necesitas instalar WeasyPrint ni librerías del sistema como Cairo, Pango o libffi.

✅ Compatible con Docker, Windows, Linux y macOS.

✅ 100% libre de dependencias nativas problemáticas.

### 5. Configura la base de datos

Abre XAMPP y activa MariaDB

Ve a phpMyAdmin y crea la base de datos:

Nombre: tienda_camisetas

No crees tablas a mano: Django se encarga de eso con migraciones.

### 6. Ejecuta migraciones y crea un superusuario

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Sigue los pasos (usuario, email, contraseña) y luego entra a /admin para configurar su perfil (UserProfile).

### 7. Corre el servidor

python manage.py runserver

Navega a: http://127.0.0.1:8000

✨ Funcionalidades

Registro e inicio de sesión de usuarios

Catálogo segmentado y filtrado por género/talla

Carrito con selección de tallas

Checkout simulado (sin pagos reales)

Descarga de boleta en PDF (HTML + imágenes externas)

Panel admin (/admin)

API REST (/api/productos/)

🛠️ Crear usuarios desde el admin
Entra a /admin

Crea un usuario (Users)

Luego crea su perfil (UserProfiles)

¡Listo! Ya puede iniciar sesión y comprar.

📁 Estructura del proyecto

RothenbergSports/
├── api_camisetas/ # No operativa, se usa una api externa con FastApi
├── app_admin/ # Administración extendida
├── app_pago/ # Lógica de compras y generación de boletas PDF
│ └── utils/ # Utilidades para PDF (Playwright)
├── ecommerce_camisetas/ # Core de la tienda
├── media/ # Imágenes locales (solo para test)
├── static/ # Archivos estáticos JS/CSS
├── tienda_camisetas/ # Proyecto principal Django
├── manage.py
├── requirements.txt
└── .gitignore
