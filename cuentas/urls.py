from django.urls import path
from .views import register, iniciosesion, exit

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', iniciosesion, name="login"),
    path('logout/', exit, name="logout"),
]

