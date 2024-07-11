from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import logout, login, authenticate
from .models import UserProfile
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.conf import settings

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            # Asigna el rol de cliente al usuario recién creado
            # Asumiendo que tienes un modelo de perfil de usuario relacionado con el usuario
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = settings.DEFAULT_USER_ROLE
            profile.save()
            login(request, user)
            return redirect('Inicio') 
    else:
        user_creation_form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': user_creation_form})

def exit(request):
    logout(request)
    return redirect('login')

def iniciosesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                request.session['perfil'] = profile.role
                login(request, user)
                return redirect('Inicio')
            except UserProfile.DoesNotExist:
                context = {
                    'error': 'Perfil de usuario no encontrado.'
                }
                return render(request, 'registration/login.html', context)
        else:
            context = {
                'error': 'Error intente denuevo'
            }
            return render(request, 'registration/login.html', context)

    return render(request, 'registration/login.html')

