from flask import Flask, render_template

app = Flask(__name__)


# ==========================================
# DATOS DEL PROYECTO
# ==========================================

# Variable simple
empresa = "Mi Empresa"


# Lista de productos con diccionarios
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


# Lista de clientes
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


# Lista de proveedores
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


# Lista de facturas
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
    productos_lista = [
        {
            "nombre": "Laptop Lenovo",
            "precio": 850.00,
            "stock": 10
        },
        {
            "nombre": "Mouse Logitech",
            "precio": 25.50,
            "stock": 5
        },
        {
            "nombre": "Teclado Mecánico",
            "precio": 75.00,
            "stock": 0
        },
        {
            "nombre": "Monitor Samsung",
            "precio": 320.00,
            "stock": 8
        }
    ]

    return render_template(
        "productos.html",
        productos=productos_lista
    )

    return render_template(
        "productos.html",
        empresa=empresa,
        productos=productos_lista
    )


# ==========================================
# MÓDULO DE CLIENTES
# ==========================================

@app.route("/clientes")
def clientes():
    clientes_lista = [
        {
            "nombre": "Juan Pérez",
            "correo": "juan@email.com",
            "estado": "Activo"
        },
        {
            "nombre": "María López",
            "correo": "maria@email.com",
            "estado": "Activo"
        },
        {
            "nombre": "Carlos Gómez",
            "correo": "carlos@email.com",
            "estado": "Inactivo"
        },
        {
            "nombre": "Ana Torres",
            "correo": "ana@email.com",
            "estado": "Activo"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )

    return render_template(
        "clientes.html",
        empresa=empresa,
        clientes=clientes_lista
    )


# ==========================================
# MÓDULO DE PROVEEDORES
# ==========================================

@app.route("/proveedores")
def proveedores():
    proveedores_lista = [
        {
            "empresa": "TecnoSuministros",
            "contacto": "Luis Andrade",
            "telefono": "0991234567"
        },
        {
            "empresa": "Distribuciones Ecuador",
            "contacto": "Sofía Morales",
            "telefono": "0987654321"
        },
        {
            "empresa": "Importadora Digital",
            "contacto": "Pedro Castillo",
            "telefono": "0976543210"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )
    


# ==========================================
# MÓDULO DE FACTURACIÓN
# ==========================================

@app.route("/facturacion")
def facturacion():
    facturas_lista = [
        {
            "numero": "FAC-001",
            "cliente": "Juan Pérez",
            "total": 125.50,
            "estado": "Pagada"
        },
        {
            "numero": "FAC-002",
            "cliente": "María López",
            "total": 280.00,
            "estado": "Pendiente"
        },
        {
            "numero": "FAC-003",
            "cliente": "Carlos Gómez",
            "total": 75.00,
            "estado": "Pagada"
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
    