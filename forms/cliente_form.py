from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=60,
                message="El nombre debe tener entre 3 y 60 caracteres."
            )
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=7,
                max=15,
                message="El teléfono debe tener entre 7 y 15 caracteres."
            )
        ]
    )

    enviar = SubmitField("Guardar cliente")