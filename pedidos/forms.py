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
    tipo_entrega = forms.ChoiceField(
        choices=Pedido.TIPO_ENTREGA_CHOICES,
        widget=forms.RadioSelect,
        initial='recoger'
    )
    notas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Pedido
        fields = ['tipo_entrega', 'notas']

class EstadoPedidoForm(forms.ModelForm):
    estado = forms.ChoiceField(
        choices=Pedido.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Pedido
        fields = ['estado']