🛍️ Rothenberg Sports
Tienda online de camisetas deportivas — Django + MariaDB + API externa

🚀 ¿Para qué sirve esto?
Tienda web con:

Catálogo dinámico (hombre, mujer, niños)

Carrito con tallas

Checkout simulado (NO hay pagos reales)

Boletas en PDF (WeasyPrint)

Registro/login de usuarios

Panel de administración

API REST de productos

Totalmente desacoplado: consume una API externa de camisetas (fácil de adaptar)

⚙️ Requisitos
Python 3.9+

XAMPP (MariaDB corriendo)

virtualenv instalado globalmente (pip install virtualenv)

Git

Dependencias nativas de WeasyPrint
(solo si vas a generar PDFs, ver instrucciones según sistema operativo)

💻 Instalación rápida

1. Clona el repositorio
   git clone https://github.com/DavidGattuso/RothenbergSports.git
   cd RothenbergSports
   code .

2. Crea y activa un entorno virtual
   Siempre usa venv como nombre de la carpeta (NO uses env).

Windows:
python -m venv venv
.\venv\Scripts\activate

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

3. Instala las dependencias del proyecto
   pip install -r requirements.txt

4. Instala dependencias nativas de WeasyPrint (PDF)
   macOS:
   brew install cairo pango gdk-pixbuf libffi

   Ubuntu/Debian:
   sudo apt-get install libpangocairo-1.0-0 libpangoft2-1.0-0 libcairo2 libffi-dev shared-mime-info

   Windows:

   - La documentación oficial de WeasyPrint fue dada de baja temporalmente.
   - Para instalar WeasyPrint y sus dependencias en Windows, busca en Google:  
     `weasyprint windows dependencies`
   - O usa las instrucciones del README del repositorio oficial:  
     https://github.com/Kozea/WeasyPrint
   - TL;DR: Necesitas instalar los binarios de Cairo, Pango y sus DLLs, y tenerlos en el PATH.

   > Busca la sección “Windows” en esa página para instalar las dependencias nativas.

   Referencia oficial (si quieres un link “vivo”):
   https://github.com/Kozea/WeasyPrint#installation

5. Configura la base de datos

   - Abre XAMPP y activa MariaDB.
   - Ve a phpMyAdmin y crea la base de datos:  
     Nombre: tienda_camisetas
   - No crees tablas a mano, Django lo hace con migraciones.

6. Ejecuta migraciones y crea un superusuario  
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

Sigue los pasos (usuario, mail, contraseña).

Después entra a /admin y edita el perfil del usuario en UserProfile.

7. Corre el servidor
   python manage.py runserver

   Navega a: http://127.0.0.1:8000

✨ Funcionalidades

- Registro e inicio de sesión de usuarios
- Catálogo segmentado y filtrado por género/talla
- Carrito con selección de tallas
- Checkout simulado (sin pagos reales)
- Descarga de boleta en PDF
- Panel admin (/admin)
- API REST (/api/productos/)

🛠️ Crear usuarios desde el admin

- Entra a /admin
- Crea usuario en Users
- Crea su perfil en UserProfiles
- Listo, ese usuario ya puede loguearse y comprar

📁 Estructura del proyecto
RothenbergSports/
├── api_camisetas/ # Lógica de consumo API externa
├── app_admin/ # Administración extendida
├── app_pago/ # Lógica de compras/boletas PDF
├── ecommerce_camisetas/ # Core de la tienda
├── media/ # Imágenes locales (para pruebas)
├── static/ # Archivos estáticos JS/CSS
├── tienda_camisetas/ # Proyecto principal Django
├── manage.py
├── requirements.txt
└── .gitignore

🔥 Notas rápidas / FAQ
Imágenes:
Se cargan desde /media/ para testeo local. Cambia esto para producción.

Pagos:
Solo flujo simulado, no pierdas tiempo buscando integraciones.

Versiones:
Funciona Django 3.1+, probado estable en 4.2.16.

API de camisetas:
El catálogo depende de una API externa. Cambia la URL si usas otra API.

PDF:
Todo con WeasyPrint. No uses xhtml2pdf, no sirve para imágenes externas ni CSS real. No pierdas tiempo probando.

🐞 Problemas típicos
"No module named 'requests'":
Activa el entorno virtual y corre:
pip install -r requirements.txt

WeasyPrint lanza error de librerías:
Instala las dependencias nativas según tu SO (ver arriba).

En Windows, WeasyPrint tira error con DLLs:
Lee la doc oficial, las rutas importan.

No conecta a MariaDB:
Revisa usuario/password/puerto en settings.py.

💡 Consejos PRO
Usa variables de entorno para credenciales en producción.

Actualiza el requirements.txt después de instalar nuevas librerías:
pip freeze > requirements.txt

Haz pruebas siempre en entorno virtual.

¿API externa cambió? Actualiza la URL en las vistas.
