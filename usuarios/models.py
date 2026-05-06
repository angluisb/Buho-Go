from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('comercio',   'Comercio'),
        ('admin',      'Administrador'),
    ]

    email = models.EmailField(unique=True)
    tipo  = models.CharField(max_length=20, choices=TIPO_CHOICES, default='estudiante')

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_tipo_display()})"