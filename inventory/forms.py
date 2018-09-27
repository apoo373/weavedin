from django.forms import ModelForm
from .models import *

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['Name', 'Value']

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ['Name', 'CostPrice', 'SellingPrice', 'Quantity']
