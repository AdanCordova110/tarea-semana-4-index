from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(message="El nombre del proveedor es obligatorio."),
            Length(min=3, max=60, message="El nombre debe tener entre 3 y 60 caracteres.")
        ]
    )

    servicio = StringField(
        "Servicio",
        validators=[
            DataRequired(message="El servicio es obligatorio."),
            Length(min=3, max=80, message="El servicio debe tener entre 3 y 80 caracteres.")
        ]
    )

    estado = StringField(
        "Estado",
        validators=[
            DataRequired(message="El estado es obligatorio."),
            Length(min=3, max=20, message="El estado debe tener entre 3 y 20 caracteres.")
        ]
    )

    enviar = SubmitField("Guardar proveedor")