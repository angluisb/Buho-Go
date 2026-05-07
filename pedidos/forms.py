from django import forms
from .models import Pedido, ItemPedido
from establecimientos.models import Producto

class ItemPedidoForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(disponible=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ItemPedido
        fields = ['producto', 'cantidad']

class PedidoForm(forms.ModelForm):
    cliente_nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'})
    )
    cliente_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    tipo_entrega = forms.ChoiceField(
        choices=Pedido.TIPO_ENTREGA_CHOICES,
        widget=forms.RadioSelect,
        initial='recoger'
    )
    notas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instrucciones especiales'})
    )

    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_email', 'tipo_entrega', 'notas']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            # Si el usuario está autenticado, ocultar campos de cliente
            self.fields['cliente_nombre'].widget = forms.HiddenInput()
            self.fields['cliente_email'].widget = forms.HiddenInput()
            # Pre-llenar con datos del usuario
            self.initial['cliente_nombre'] = f"{self.user.first_name} {self.user.last_name}".strip()
            self.initial['cliente_email'] = self.user.email

class EstadoPedidoForm(forms.ModelForm):
    estado = forms.ChoiceField(
        choices=Pedido.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Pedido
        fields = ['estado']