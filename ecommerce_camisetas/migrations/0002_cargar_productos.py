from django.db import migrations

def cargar_productos_y_tallas(apps, schema_editor):
    Producto = apps.get_model('ecommerce_camisetas', 'Producto')
    Categoria = apps.get_model('ecommerce_camisetas', 'Categoria')
    TallaProducto = apps.get_model('ecommerce_camisetas', 'TallaProducto')

    # Crear las categorías
    categoria_hombre, created = Categoria.objects.get_or_create(nombre='Hombre')
    categoria_mujer, created = Categoria.objects.get_or_create(nombre='Mujer')
    categoria_ninos, created = Categoria.objects.get_or_create(nombre='Niños')

    # Crear los productos
    productos = [
        {
            'nombre': 'Camiseta Local Hombre Portugal',
            'descripcion': 'Camiseta oficial Portugal con el nombre de Ronaldo',
            'precio': 79990,
            'imagen': 'img/c_hombre/ronaldo.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Visita Mujer Colo Colo',
            'descripcion': 'Camiseta oficial del equipo Coco Colo',
            'precio': 65990,
            'imagen': 'img/c_mujer/colocolof.jpg',
            'categoria': categoria_mujer
        },
        {
            'nombre': 'Camiseta Local Niño Juventus',
            'descripcion': 'Camiseta oficial del equipo Juventus para niños',
            'precio': 43990,
            'imagen': 'img/c_ninos/juventusn.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Local Hombre Argentina',
            'descripcion': 'Camiseta oficial Argentina con el nombre de Messi',
            'precio': 79990,
            'imagen': 'img/c_hombre/messi.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Inter Miami',
            'descripcion': 'Camiseta oficial del equipo Inter Miami',
            'precio': 59990,
            'imagen': 'img/c_hombre/intermiami.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Colo Colo',
            'descripcion': 'Camiseta oficial del equipo Colo Colo',
            'precio': 59990,
            'imagen': 'img/c_hombre/colocolo.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Universidad de Chile',
            'descripcion': 'Camiseta oficial del equipo Universidad de Chile',
            'precio': 46990,
            'imagen': 'img/c_hombre/udechile.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Universidad Catolica',
            'descripcion': 'Camiseta oficial del equipo Universidad Católica',
            'precio': 52990,
            'imagen': 'img/c_hombre/catolica.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Barcelona',
            'descripcion': 'Camiseta oficial del equipo Barcelona',
            'precio': 54990,
            'imagen': 'img/c_hombre/barcelona.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Real Madrid',
            'descripcion': 'Camiseta oficial del equipo Real Madrid',
            'precio': 69990,
            'imagen': 'img/c_hombre/realmadrid.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Atletico de Madrid',
            'descripcion': 'Camiseta oficial del equipo Atletico de Madrid',
            'precio': 64990,
            'imagen': 'img/c_hombre/atleticom.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Manchester City',
            'descripcion': 'Camiseta oficial del equipo Manchester City',
            'precio': 67990,
            'imagen': 'img/c_hombre/manchestercity.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Manchester United',
            'descripcion': 'Camiseta oficial del equipo Manchester United',
            'precio': 64990,
            'imagen': 'img/c_hombre/manchesterunited.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre AC Milan',
            'descripcion': 'Camiseta oficial del equipo AC Milan',
            'precio': 62990,
            'imagen': 'img/c_hombre/acmilan.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Brasil',
            'descripcion': 'Camiseta oficial de la selección de Brasil',
            'precio': 71990,
            'imagen': 'img/c_hombre/brasil.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Chile',
            'descripcion': 'Camiseta oficial de la selección de Chile',
            'precio': 69990,
            'imagen': 'img/c_hombre/chile.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Local Hombre Francia',
            'descripcion': 'Camiseta oficial de la selección de Francia',
            'precio': 72990,
            'imagen': 'img/c_hombre/francia.jpg',
            'categoria': categoria_hombre
        },
        {
            'nombre': 'Camiseta Visita Mujer Chile',
            'descripcion': 'Camiseta oficial de la seleccion chilena',
            'precio': 59990,
            'imagen': 'img/c_mujer/chilef.jpg',
            'categoria': categoria_mujer
        },
        {
            'nombre': 'Camiseta Visita Mujer Chile',
            'descripcion': 'Camiseta oficial del equipo Universidad de Chile',
            'precio': 59990,
            'imagen': 'img/c_mujer/udechilef.jpg',
            'categoria': categoria_mujer
        },
        {
            'nombre': 'Camiseta Local Mujer Bayern Munich',
            'descripcion': 'Camiseta oficial del equipo Bayern Munich de Alemania',
            'precio': 56990,
            'imagen': 'img/c_mujer/bayernm.jpg',
            'categoria': categoria_mujer
        },
        {
            'nombre': 'Camiseta Local Mujer Alemania',
            'descripcion': 'Camiseta oficial de la selección de Alemania',
            'precio': 44990,
            'imagen': 'img/c_mujer/alemaniaf.jpg',
            'categoria': categoria_mujer
        },
        {
            'nombre': 'Camiseta Local Mujer Argentina',
            'descripcion': 'Camiseta oficial de la selección de Argentina',
            'precio': 42990,
            'imagen': 'img/c_mujer/argentinaf.jpg',
            'categoria': categoria_mujer
        },
        {
            'nombre': 'Camiseta Local Niño Argentina',
            'descripcion': 'Camiseta oficial de la selección de Argentina para niños',
            'precio': 39990,
            'imagen': 'img/c_ninos/argentinan.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Local Niño Manchester United',
            'descripcion': 'Camiseta oficial del equipo Manchester United para niños',
            'precio': 49990,
            'imagen': 'img/c_ninos/manunitedn.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Local Niño Chile',
            'descripcion': 'Camiseta oficial de la selección de Chile para niños',
            'precio': 49990,
            'imagen': 'img/c_ninos/chilen.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Local Niño Colo Colo',
            'descripcion': 'Camiseta oficial del equipo Colo Colo para niños',
            'precio': 49990,
            'imagen': 'img/c_ninos/colocolon.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Local Niño Universidad de Chile',
            'descripcion': 'Camiseta oficial del equipo Universidad de Chile para niños',
            'precio': 39990,
            'imagen': 'img/c_ninos/udechilen.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Reversible Gxrt1ß Niño',
            'descripcion': 'Camiseta deportiva reversible para niños',
            'precio': 19990,
            'imagen': 'img/c_ninos/camiseta1.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Reversible Gxrt2ß Niño',
            'descripcion': 'Camiseta deportiva reversible para niños',
            'precio': 19990,
            'imagen': 'img/c_ninos/camiseta2.jpg',
            'categoria': categoria_ninos
        },
        {
            'nombre': 'Camiseta Reversible Gxrt3ß Niño',
            'descripcion': 'Camiseta deportiva reversible para niños',
            'precio': 19990,
            'imagen': 'img/c_ninos/camiseta3.jpg',
            'categoria': categoria_ninos
        }
    ]

    # Crear productos y sus tallas
    for producto_data in productos:
        producto = Producto.objects.create(**producto_data)
        
        # Asignar tallas según categoría
        if producto.categoria == categoria_hombre:
            tallas = ['S', 'M', 'L', 'XL']
        elif producto.categoria == categoria_mujer:
            tallas = ['XS', 'S', 'M', 'L', 'XL']
        else:
            tallas = ['XS', 'S', 'M', 'L']

        for talla in tallas:
            TallaProducto.objects.create(producto=producto, talla=talla)


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_camisetas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_productos_y_tallas),
    ]
