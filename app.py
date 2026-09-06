import sqlite3
import os

from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-semana-11"

# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "ferreteria.db")


def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tabla_productos():
    conn = conectar_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# DATOS DEL PROYECTO
# ==========================================

empresa = "Mi Empresa"


# PRODUCTOS



# CLIENTES
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


# PROVEEDORES
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


# FACTURAS
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
# MÓDULO DE PRODUCTOS
# ==========================================

@app.route("/productos")
def productos():

    conn = conectar_db()

    productos_db = conn.execute(
        "SELECT * FROM productos"
    ).fetchall()

    conn.close()

    return render_template(
        "productos.html",
        empresa=empresa,
        productos=productos_db
    )


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = conectar_db()

        conn.execute(
            """
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
            """,
            (
                form.nombre.data,
                form.categoria.data,
                float(form.precio.data),
                form.stock.data
            )
        )

        conn.commit()
        conn.close()

        flash(
            "Producto guardado correctamente en la base de datos.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


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


@app.route("/clientes/nuevo", methods=["GET", "POST"])
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


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
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


@app.route("/facturacion/nueva", methods=["GET", "POST"])
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
    crear_tabla_productos()
    app.run(debug=True)