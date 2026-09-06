from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):
    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres.")
        ]
    )

    categoria = StringField(
        "Categoría",
        validators=[
            DataRequired(message="La categoría es obligatoria."),
            Length(min=3, max=40, message="La categoría debe tener entre 3 y 40 caracteres.")
        ]
    )

    precio = DecimalField(
        "Precio",
        places=2,
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor que 0.")
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(min=0, message="El stock no puede ser negativo.")
        ]
    )

    enviar = SubmitField("Guardar producto")