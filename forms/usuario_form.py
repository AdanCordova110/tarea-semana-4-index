from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UsuarioForm(FlaskForm):

    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(min=4, max=100)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=6, max=100)
        ]
    )

    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Las contraseñas deben coincidir."
            )
        ]
    )

    enviar = SubmitField("Registrarse")