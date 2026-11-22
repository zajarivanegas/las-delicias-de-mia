from django import forms
from django.contrib.auth.models import User


class RegistroClienteForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        error_messages={"required": "Escribe tu nombre."}
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        error_messages={
            "required": "Escribe tu correo.",
            "invalid": "Ingresa un correo válido."
        }
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        error_messages={"required": "Escribe tu teléfono."}
    )
    password = forms.CharField(
        label="Contraseña",
        max_length=8,
        widget=forms.PasswordInput,
        error_messages={
            "required": "Escribe una contraseña.",
            "max_length": "Máximo 8 caracteres."
        }
    )
    confirmar_password = forms.CharField(
        label="Confirmar contraseña",
        max_length=8,
        widget=forms.PasswordInput,
        error_messages={"required": "Confirma tu contraseña."}
    )

    def clean_correo(self):
        correo = self.cleaned_data.get("correo", "").strip().lower()
        if User.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Ese correo ya está registrado.")
        return correo

    def clean(self):
        datos = super().clean()
        clave = datos.get("password")
        confirmacion = datos.get("confirmar_password")

        if clave and len(clave) > 8:
            self.add_error("password", "La contraseña no puede pasar de 8 caracteres.")

        if clave and confirmacion and clave != confirmacion:
            self.add_error("confirmar_password", "Las contraseñas no coinciden.")

        return datos

class LoginForm(forms.Form):
    correo = forms.EmailField(
        label="Correo electrónico",
        error_messages={
            "required": "Debes ingresar tu correo.",
            "invalid": "Ingresa un correo válido."
        }
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        error_messages={"required": "Debes ingresar tu contraseña."}
    )