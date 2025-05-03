
🛍️ Rothenberg Sports

Tienda online de camisetas deportivas desarrollada con Django.
Incluye: catálogo, carrito, pagos simulados, administración de usuarios, boletas en PDF y una API REST.

⚙️ Requisitos previos

🐍 Python 3.9 o superior
🧱 XAMPP con MariaDB activo
📦 virtualenv instalado globalmente
💻 Instalación (Entorno Virtual)

1️⃣ Clonar el repositorio
git clone https://github.com/tu-usuario/RothenbergSports.git
cd RothenbergSports
2️⃣ Crear y activar entorno virtual
python -m venv env
En Windows:
.\env\Scripts\activate
En macOS/Linux:
source env/bin/activate
3️⃣ Instalar dependencias desde requirements.txt
pip install -r requirements.txt
🛠️ Configuración inicial

🧩 Crear base de datos en XAMPP
Abre phpMyAdmin
Crea una base de datos llamada:
tienda_camisetas
🔄 Aplicar migraciones
python manage.py makemigrations
python manage.py migrate
👤 Crear superusuario
python manage.py createsuperuser
Ejemplo:
Usuario: admin
Contraseña: 1234
👉 Luego, entra a /admin y asócialo en el modelo UserProfile.

▶️ Ejecutar el proyecto

python manage.py runserver
Navega a:
http://127.0.0.1:8000

✨ Funcionalidades clave

👥 Registro e inicio de sesión
👕 Catálogo segmentado (hombre, mujer, niños)
🛒 Carrito con selección de tallas
💳 Proceso de compra simulado
🧾 Generación de boleta en PDF
🔐 Panel administrativo
🔌 API REST: /api/productos/
🔧 Crear usuarios desde el administrador

Ve a /admin
Crea un usuario en Users
Luego crea su perfil en UserProfiles
✅ Ahora ese usuario podrá iniciar sesión y comprar.

📁 Estructura del proyecto

RothenbergSports/
├── api_camisetas/
├── app_admin/
├── app_pago/
├── ecommerce_camisetas/
├── media/              # Imágenes locales
├── static/             # Archivos JS/CSS
├── tienda_camisetas/   # Proyecto principal Django
├── manage.py
├── requirements.txt
└── .gitignore
📝 Notas importantes

🖼️ Las imágenes están en /media/ para facilitar pruebas locales
🚫 No hay pasarela de pago real (es solo flujo simulado)
🛠️ Compatible con Django 3.1 en adelante (probado en 4.2.16)
