from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ModificarUsuarioForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from MyApp.forms import PasswordResetRequestForm
from django.utils import timezone
from datetime import timedelta
from .forms import PasswordResetRequestForm
from django.core.mail import send_mail
from .forms import ContactForm
from .models import Photo

def tu_vista(request):
    # Obtener todas las fotos desde la base de datos
    photos = Photo.objects.all()
    
    # Pasar las fotos a la plantilla como parte del contexto
    context = {
        'photos': photos
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'fotos.html', context)


def home(request):
    return render(request, "index.html")


class RegistroView(FormView):
    template_name = "inicio/registro1.html"
    form_class = RegistroForm
    success_url = reverse_lazy("inicio-sesion")
    success_message = "Usuario registrado exitosamente."

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Usuario registrado exitosamente.")
        return super().form_valid(form)


class InicioSesionView(FormView):
    template_name = "inicio/inicio-sesion1.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy(
        "Home"
    )  # URL a la que redirigir despues del inicio de sesion

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


#def logout_view(request):
#   logout(request)
#  return redirect("Home")

from django.shortcuts import redirect

def logout_view(request):
    response = redirect('Home')
    response.delete_cookie('sessionid')  # Borra la cookie de sesión
    return response



def indio(request):
    return render(request, "indio.html")


def LaRenga(request):
    return render(request, "LaRenga.html")


def Divididos(request):
    return render(request, "Divididos.html")


def Ciro(request):
    return render(request, "ciro.html")


def ntvg(request):
    return render(request, "ntvg.html")


def LasPelotas(request):
    return render(request, "LasPelotas.html")


# esto modifica los datos del usuario
# *********************************************#
@login_required  # Requiere que el usuario esté autenticado
def modificar_datos_usuario(request):
    usuario = request.user  # Obtiene el usuario actual
    if request.method == "POST":  # Si el método es POST
        form = ModificarUsuarioForm(
            request.POST, instance=usuario
        )  # Crea un formulario con los datos del usuario
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda los cambios
            return redirect(
                "modificar_datos_usuario"
            )  # Redirige al perfil del usuario después de la modificación
    else:
        form = ModificarUsuarioForm(instance=usuario)
    return render(request, "inicio/modifica-usuario.html", {"form": form})


# ****************************************************************#


# Vista para el Proceso de Olvido de Contraseña:
# **********************************************#

def forgot_password(request):
    if request.method == "POST":   
        form = PasswordResetRequestForm(request.POST) 
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None: 
                # Generar token de restablecimiento de contraseña
                token = get_random_string(length=32)
                user.password_reset_token = token 
                user.password_reset_token_created = timezone.now()
                user.save()
                # Enviar correo electrónico con el enlace de restablecimiento
                send_mail(
                    "Restablecer contraseña",
                    "Sigue este enlace para restablecer tu contraseña: http://127.0.0.1:8000/restablecer-password/{}/".format(
                        token
                    ),
                    "kraquen8686@gmail.com", 
                    [email],
                    fail_silently=False,
                )
                return redirect("inicio-sesion")
    else:
        form = PasswordResetRequestForm()
    return render(request, "olvido-contraseña.html", {"form": form})


#vista formulario de contacto 

def FormContacto(request):
    return render(request, 'formulario-de-contacto.html')

#**********************************************#
#vista para capturar los datos y enviar al mail 

def contacto(request):
    if request.method=='POST':

        miFormulario = ContactForm(request.POST)

        if miFormulario.is_valid():
            infForm = miFormulario.cleaned_data
            send_mail(infForm['nombre'],infForm['mensaje'], infForm.get('email', ' '),['kraquen8686@gmail.com'])
            return render(request,'gracias.html')
    else:
        miFormulario=ContactForm()
        
        return render(request, 'formulario-de-contacto.html', {'form':miFormulario})
    

def gracais(request):
    return render(request, 'gracias.html')

def QuienesSomos(request):
    return render(request,'quienes_somos.html')


