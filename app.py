from flask import Flask, render_template, redirect, url_for, flash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from models import Usuario

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion import obtener_conexion
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-semana-11"

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def cargar_usuario(id_usuario):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT id_usuario, username, password_hash
        FROM usuarios
        WHERE id_usuario = %s
        """,
        (id_usuario,)
    )

    usuario_db = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario_db is None:
        return None

    return Usuario(
        usuario_db["id_usuario"],
        usuario_db["username"],
        usuario_db["password_hash"]
    )

# ==========================================
# PROBAR CONEXIÓN POSTGRESQL
# ==========================================

def probar_conexion():
    try:
        conexion = obtener_conexion()
        print("Conexión a PostgreSQL exitosa.")
        conexion.close()

    except Exception as error:
        print("Error al conectar con PostgreSQL:")
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
# AUTENTICACIÓN DE USUARIOS
# ==========================================

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = UsuarioForm()

    if form.validate_on_submit():
        conexion = obtener_conexion()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)

        # Comprobar que el nombre de usuario no esté registrado
        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE username = %s",
            (form.username.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conexion.close()

            flash(
                "El nombre de usuario ya está registrado.",
                "warning"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Proteger la contraseña antes de guardarla
        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute(
            """
            INSERT INTO usuarios (username, password_hash)
            VALUES (%s, %s)
            """,
            (
                form.username.data,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        conexion = obtener_conexion()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id_usuario, username, password_hash
            FROM usuarios
            WHERE username = %s
            """,
            (form.username.data,)
        )

        usuario_db = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario_db and check_password_hash(
            usuario_db["password_hash"],
            form.password.data
        ):
            usuario = Usuario(
                usuario_db["id_usuario"],
                usuario_db["username"],
                usuario_db["password_hash"]
            )

            login_user(usuario)

            flash(
                f"Bienvenido, {usuario.username}.",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        empresa=empresa
    )

# ==========================================
# # MÓDULO DE PRODUCTOS - POSTGRESQL
# ==========================================

@app.route("/productos")
def productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

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
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

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
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

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
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

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
@login_required
def clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id_cliente, nombre, correo, telefono
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        empresa=empresa,
        clientes=clientes_db
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO clientes (nombre, correo, telefono)
            VALUES (%s, %s, %s)
        """

        valores = (
            form.nombre.data,
            form.correo.data,
            form.telefono.data
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

@app.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
@login_required
def editar_cliente(id_cliente):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM clientes WHERE id_cliente = %s",
        (id_cliente,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    if cliente is None:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("clientes"))

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE clientes
            SET nombre = %s,
                correo = %s,
                telefono = %s
            WHERE id_cliente = %s
        """

        valores = (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            id_cliente
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Cliente modificado correctamente.", "success")
        return redirect(url_for("clientes"))

    if not form.is_submitted():
        form.nombre.data = cliente["nombre"]
        form.correo.data = cliente["correo"]
        form.telefono.data = cliente["telefono"]

    return render_template(
        "formulario_cliente.html",
        form=form,
        editando=True
    )

@app.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
@login_required
def eliminar_cliente(id_cliente):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM clientes WHERE id_cliente = %s",
        (id_cliente,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes"))

# ==========================================
# MÓDULO DE PROVEEDORES
# ==========================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id_proveedor, nombre, servicio, estado
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        empresa=empresa,
        proveedores=proveedores_db
    )

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO proveedores (nombre, servicio, estado)
            VALUES (%s, %s, %s)
        """

        valores = (
            form.nombre.data,
            form.servicio.data,
            form.estado.data
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

@app.route("/proveedores/editar/<int:id_proveedor>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT * FROM proveedores WHERE id_proveedor = %s",
        (id_proveedor,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    if proveedor is None:
        flash("Proveedor no encontrado.", "danger")
        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                servicio = %s,
                estado = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.servicio.data,
            form.estado.data,
            id_proveedor
        ))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Proveedor modificado correctamente.", "success")

        return redirect(url_for("proveedores"))

    if not form.is_submitted():
        form.nombre.data = proveedor["nombre"]
        form.servicio.data = proveedor["servicio"]
        form.estado.data = proveedor["estado"]

    return render_template(
        "formulario_proveedor.html",
        form=form,
        editando=True
    )

@app.route("/proveedores/eliminar/<int:id_proveedor>", methods=["POST"])
@login_required
def eliminar_proveedor(id_proveedor):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM proveedores WHERE id_proveedor = %s",
        (id_proveedor,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Buscar el cliente por su nombre
        cursor.execute(
            "SELECT id_cliente FROM clientes WHERE nombre = %s",
            (form.cliente.data,)
        )

        cliente = cursor.fetchone()

        if cliente is None:
            cursor.close()
            conexion.close()

            flash(
                "El cliente seleccionado no existe en la base de datos.",
                "danger"
            )

            return render_template(
                "formulario_facturacion.html",
                form=form
            )

        id_cliente = cliente[0]

        # Registrar la factura relacionada con el cliente
        cursor.execute("""
            INSERT INTO facturas
                (numero, id_cliente, total, estado)
            VALUES
                (%s, %s, %s, %s)
        """, (
            form.numero.data,
            id_cliente,
            float(form.total.data),
            form.estado.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )

@app.route("/facturacion/editar/<int:id_factura>", methods=["GET", "POST"])
@login_required
def editar_factura(id_factura):

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero,
            c.nombre AS cliente,
            f.total,
            f.estado
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        WHERE f.id_factura = %s
    """, (id_factura,))

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()

    if factura is None:
        flash("Factura no encontrada.", "danger")
        return redirect(url_for("facturacion"))

    form = FacturacionForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Buscar el ID del cliente
        cursor.execute(
            "SELECT id_cliente FROM clientes WHERE nombre = %s",
            (form.cliente.data,)
        )

        cliente = cursor.fetchone()

        if cliente is None:
            cursor.close()
            conexion.close()

            flash("El cliente indicado no existe.", "danger")

            return render_template(
                "formulario_facturacion.html",
                form=form,
                editando=True
            )

        id_cliente = cliente[0]

        cursor.execute("""
            UPDATE facturas
            SET numero = %s,
                id_cliente = %s,
                total = %s,
                estado = %s
            WHERE id_factura = %s
        """, (
            form.numero.data,
            id_cliente,
            float(form.total.data),
            form.estado.data,
            id_factura
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Factura modificada correctamente.", "success")

        return redirect(url_for("facturacion"))

    if not form.is_submitted():
        form.numero.data = factura["numero"]
        form.cliente.data = factura["cliente"]
        form.total.data = factura["total"]
        form.estado.data = factura["estado"]

    return render_template(
        "formulario_facturacion.html",
        form=form,
        editando=True
    )


@app.route("/facturacion/eliminar/<int:id_factura>", methods=["POST"])
@login_required
def eliminar_factura(id_factura):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM facturas WHERE id_factura = %s",
        (id_factura,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Factura eliminada correctamente.", "success")

    return redirect(url_for("facturacion"))

# ==========================================
# MÓDULO DE FACTURACIÓN
# ==========================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero,
            c.nombre AS cliente,
            f.total,
            f.estado
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura
    """)

    facturas_db = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        empresa=empresa,
        facturas=facturas_db
    )

# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    probar_conexion()

    app.run(debug=True)