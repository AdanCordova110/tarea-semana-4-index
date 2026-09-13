from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion import obtener_conexion


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-semana-11"


# ==========================================
# PROBAR CONEXIÓN MYSQL
# ==========================================

def probar_conexion():
    try:
        conexion = obtener_conexion()
        print("Conexión a MySQL exitosa. - app.py:22")
        conexion.close()
    except Exception as error:
        print("Error al conectar con MySQL: - app.py:25")
        print(error)


# ==========================================
# DATOS DEL PROYECTO
# ==========================================

empresa = "Mi Empresa"


# ==========================================
# CLIENTES TEMPORALES
# ==========================================

clientes_lista = [
    {
        "nombre": "Carlos Mendoza",
        "correo": "carlos@email.com",
        "telefono": "0991234567"
    },
    {
        "nombre": "María López",
        "correo": "maria@email.com",
        "telefono": "0987654321"
    },
    {
        "nombre": "Juan Pérez",
        "correo": "juan@email.com",
        "telefono": "0974561238"
    }
]


# ==========================================
# PROVEEDORES TEMPORALES
# ==========================================

proveedores_lista = [
    {
        "nombre": "Tech Solutions",
        "servicio": "Equipos informáticos",
        "estado": "Activo"
    },
    {
        "nombre": "Digital Store",
        "servicio": "Accesorios tecnológicos",
        "estado": "Activo"
    },
    {
        "nombre": "Servicios Web EC",
        "servicio": "Servicios digitales",
        "estado": "Pendiente"
    }
]


# ==========================================
# FACTURAS TEMPORALES
# ==========================================

facturas_lista = [
    {
        "numero": "FAC-001",
        "cliente": "Carlos Mendoza",
        "total": 250.00,
        "estado": "Pagada"
    },
    {
        "numero": "FAC-002",
        "cliente": "María López",
        "total": 450.00,
        "estado": "Pendiente"
    },
    {
        "numero": "FAC-003",
        "cliente": "Juan Pérez",
        "total": 120.00,
        "estado": "Pagada"
    }
]


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    mensaje_bienvenida = "Bienvenido a Mi Empresa"

    return render_template(
        "index.html",
        empresa=empresa,
        mensaje_bienvenida=mensaje_bienvenida
    )


# ==========================================
# MÓDULO DE PRODUCTOS - MYSQL
# ==========================================

@app.route("/productos")
def productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.categoria,
            p.precio,
            p.stock,
            p.id_proveedor,
            pr.nombre AS proveedor_nombre
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
    """)

    productos_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        empresa=empresa,
        productos=productos_db
    )


# ==========================================
# AGREGAR PRODUCTO - INSERT
# ==========================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_proveedor, nombre FROM proveedores"
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO productos
            (nombre, categoria, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            form.nombre.data,
            form.categoria.data,
            float(form.precio.data),
            form.stock.data,
            form.id_proveedor.data
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================
# EDITAR PRODUCTO - UPDATE
# ==========================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto = cursor.fetchone()

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    if producto is None:

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(url_for("productos"))

    form = ProductoForm()

    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """

        valores = (
            form.nombre.data,
            form.categoria.data,
            float(form.precio.data),
            form.stock.data,
            form.id_proveedor.data,
            id_producto
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto modificado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

        if producto["id_proveedor"] is not None:
            form.id_proveedor.data = producto["id_proveedor"]

    return render_template(
        "formulario_producto.html",
        form=form,
        editando=True
    )
# ==========================================
# ELIMINAR PRODUCTO - DELETE
# ==========================================

@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
def eliminar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect(url_for("productos"))


# ==========================================
# MÓDULO DE CLIENTES
# ==========================================

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        empresa=empresa,
        clientes=clientes_lista
    )


@app.route(
    "/clientes/nuevo",
    methods=["GET", "POST"]
)
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        clientes_lista.append(cliente)

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==========================================
# MÓDULO DE PROVEEDORES
# ==========================================

@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        empresa=empresa,
        proveedores=proveedores_lista
    )


@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "nombre": form.nombre.data,
            "servicio": form.servicio.data,
            "estado": form.estado.data
        }

        proveedores_lista.append(proveedor)

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================
# MÓDULO DE FACTURACIÓN
# ==========================================

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        empresa=empresa,
        facturas=facturas_lista
    )


@app.route(
    "/facturacion/nueva",
    methods=["GET", "POST"]
)
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": float(form.total.data),
            "estado": form.estado.data
        }

        facturas_lista.append(factura)

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    probar_conexion()

    app.run(debug=True)