from django.contrib import admin
from django.urls import path, include

from establecimientos.views import home

urlpatterns = [

    path('', home, name='home'),

    path('admin/', admin.site.urls),

    path('establecimientos/', include('establecimientos.urls')),

    path('pedidos/', include('pedidos.urls')),

    path('usuarios/', include('usuarios.urls')),
]