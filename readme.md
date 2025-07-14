# 🛍️ Rothenberg Sports

**Tienda online de camisetas deportivas**  
_Django + MariaDB + API externa_

---

## 🚀 ¿Qué hace este proyecto?

- **Catálogo dinámico** (hombre, mujer, niños)
- **Carrito** con selección de tallas
- **Checkout simulado** _(NO pagos reales)_
- **Boletas en PDF** (Playwright + Chromium headless)
- **Registro/Login** de usuarios
- **Panel de administración**
- **API REST** de productos
- **Totalmente desacoplado**: consume una API externa de camisetas

---

## ⚙️ Requisitos

- Python 3.9+
- XAMPP (MariaDB corriendo)
- `virtualenv` instalado globalmente (`pip install virtualenv`)
- Git

---

## 💻 Instalación rápida

### 1. Clona el repositorio y entra a la carpeta

git clone https://github.com/DavidGattuso/RothenbergSports.git

cd RothenbergSports

code .

2. Crea y activa un entorno virtual (venv)
<details> <summary>Windows</summary>

python -m venv venv
.\venv\Scripts\activate
</details> <details> <summary>macOS / Linux</summary>

python3 -m venv venv
source venv/bin/activate
</details>
3. Instala las dependencias del proyecto

pip install -r requirements.txt

4. Instala los navegadores de Playwright (solo una vez)

python -m playwright install

Esto es obligatorio para generar PDFs con Chromium headless.
NO necesitas instalar WeasyPrint ni librerías nativas.

🛠️ Configuración de la base de datos
Abre XAMPP y activa MariaDB.

Ve a phpMyAdmin y crea la base de datos llamada:

tienda_camisetas
NO crees tablas a mano: Django se encarga de todo con migraciones.

🗂️ Migraciones y usuario admin

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Sigue los pasos: usuario, email, contraseña.

▶️ Corre el servidor

python manage.py runserver
Abre http://127.0.0.1:8000 en tu navegador.

✨ Funcionalidades
Registro e inicio de sesión de usuarios

Catálogo segmentado y filtrado por género/talla

Carrito con selección de tallas

Checkout simulado (sin pagos reales)

Descarga de boleta en PDF (HTML + imágenes externas)

Panel admin (/admin)

API REST (/api/productos/)

👤 Crear usuarios desde el admin
Entra a /admin

Crea un usuario (Users)

Luego crea su perfil (UserProfiles)

¡Listo! Ya puedes iniciar sesión y comprar.

📁 Estructura del proyecto

RothenbergSports/
├── app_admin/               # Administración extendida
├── app_pago/                # Lógica de compras y generación de boletas PDF
│   └── utils/               # Utilidades para PDF (Playwright)
├── ecommerce_camisetas/     # Core de la tienda
├── media/                   # Imágenes locales (solo test)
├── static/                  # Archivos estáticos JS/CSS
├── tienda_camisetas/        # Proyecto principal Django
├── manage.py
├── requirements.txt
└── .gitignore