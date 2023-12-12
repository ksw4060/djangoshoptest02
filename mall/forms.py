from django import forms
from .models import CartProduct, Product


class CartProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = [
            "quantity",
        ]


    """def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        product = self.instance.product
        if quantity > product.stock:
            raise forms.ValidationError("재고가 부족합니다.")
        return quantity"""
