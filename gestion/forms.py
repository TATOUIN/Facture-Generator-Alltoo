from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'prix', 'date_peremption']
        widgets = {
            'date_peremption': forms.DateInput(attrs={
                'type': 'date',
                'min': '2025-01-01',
                'max': '2030-12-12',
                'id': 'start',
                'name': 'trip-start',
            }),
        }
