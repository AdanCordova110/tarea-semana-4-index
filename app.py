from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-semana-11"


# ==========================================
# DATOS DEL PROYECTO
# ==========================================

empresa = "Mi Empresa"


# PRODUCTOS
productos_lista = [
    {
        "nombre": "Diseño Web",
        "precio": 250.00,
        "stock": 10,
        "categoria": "Desarrollo"
    },
    {
        "nombre": "Desarrollo Web",
        "precio": 450.00,
        "stock": 5,
        "categoria": "Desarrollo"
    },
    {
        "nombre": "Soporte Técnico",
        "precio": 80.00,
        "stock": 0,
        "categoria": "Soporte"
    },
    {
        "nombre": "Mantenimiento Web",
        "precio": 120.00,
        "stock": 8,
        "categoria": "Mantenimiento"
    }
]


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

    return render_template(
        "productos.html",
        empresa=empresa,
        productos=productos_lista
    )


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": float(form.precio.data),
            "stock": form.stock.data
        }

        productos_lista.append(producto)

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
    app.run(debug=True)