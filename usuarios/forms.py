from django import forms
from django.contrib.auth import authenticate
from .models import Usuario


class RegistroClienteForm(forms.Form):
    """Formulario de registro (HU-01).

    OJO: aquí NO existe el campo "rol". Así el usuario nunca puede elegirlo (criterio f).
    """

    # Criterio a: nombre, correo, teléfono y contraseña (+ confirmación)
    nombre = forms.CharField(
        max_length=150,
        error_messages={"required": "Escribe tu nombre."},
    )
    correo = forms.EmailField(
        error_messages={
            "required": "Escribe tu correo.",
            "invalid": "El correo no es válido. Ejemplo: nombre@correo.com",
        },
    )
    telefono = forms.RegexField(
        regex=r"^[0-9]{7,10}$",
        error_messages={
            "required": "Escribe tu teléfono.",
            "invalid": "El teléfono debe tener solo números (de 7 a 10 dígitos).",
        },
    )
    # Criterio c: contraseña de máximo 8 caracteres
    password = forms.CharField(
        max_length=8,
        widget=forms.PasswordInput,
        error_messages={
            "required": "Escribe una contraseña.",
            "max_length": "La contraseña puede tener máximo 8 caracteres.",
        },
    )
    confirmar = forms.CharField(
        max_length=8,
        widget=forms.PasswordInput,
        error_messages={
            "required": "Confirma tu contraseña.",
            "max_length": "La contraseña puede tener máximo 8 caracteres.",
        },
    )

    # Criterio b: no permitir un correo que ya existe
    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip().lower()
        if Usuario.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado. Usa otro o inicia sesión."
            )
        return correo

    # Criterio c: las dos contraseñas deben ser iguales
    def clean(self):
        datos = super().clean()
        password = datos.get("password")
        confirmar = datos.get("confirmar")
        if password and confirmar and password != confirmar:
            self.add_error("confirmar", "Las contraseñas no son iguales.")
        return datos

    # Guarda al cliente en la base de datos
    def guardar(self):
        datos = self.cleaned_data
        return Usuario.objects.create_user(
            username=datos["correo"],      # usamos el correo como nombre de usuario
            email=datos["correo"],
            password=datos["password"],    # create_user la encripta sola
            first_name=datos["nombre"],
            telefono=datos["telefono"],
            rol=Usuario.Rol.CLIENTE,       # el rol lo pone el programa, no el usuario
        )

class LoginForm(forms.Form):
    correo = forms.EmailField(
        error_messages={
            "required": "Escribe tu correo.",
            "invalid": "El correo no es válido. Ejemplo: nombre@correo.com",
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={"required": "Escribe tu contraseña."},
    )

    def clean(self):
        datos = super().clean()
        correo = datos.get("correo")
        password = datos.get("password")

        if correo and password:
            usuario = None
            usuario_db = Usuario.objects.filter(email__iexact=correo).first()
            if usuario_db:
                usuario = authenticate(username=usuario_db.username, password=password)

            if usuario is None:
                # Criterio 2: mensaje claro, sin decir cuál de los dos datos falló
                raise forms.ValidationError("Correo o contraseña incorrectos.")
            self.usuario = usuario

        return datos