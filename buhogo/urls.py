from django.contrib import admin
from django.urls import path, include
from establecimientos.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('pedidos/', include('pedidos.urls')),
    path('establecimientos/', include('establecimientos.urls')),
    path('usuarios/', include('usuarios.urls')),
]