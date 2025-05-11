from django import forms
from .models import Supplier, Buyer, Product, Order

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class SellerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Supplier
        fields = ['name', 'contact','email','password']

class BuyerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Buyer
        fields = ['name', 'email', 'phone','password']

class SellerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class BuyerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'stock', 'price']


class AddOrderForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Select Product')
    quantity = forms.IntegerField(min_value=1, label='Quantity')
