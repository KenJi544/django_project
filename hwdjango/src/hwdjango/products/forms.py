from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Type in the title !*'
            }
        ))
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          'placeholder': 'Type the description',
                                          'rows': 20,
                                          'cols': 150,
                                          }
                                      ))
    price = forms.DecimalField(initial=0.00)

    class Meta:
        model = Product
        fields = {
                'title',
                'description',
                'price'
                }

    def clean_price(self, *args, **kwargs):
        price = self.cleaned_data.get('price')
        if price < 0.0:
            raise forms.ValidationError('Not a valid price')
        return price


class RawProductForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Type in the title !*'
            }
        ))
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          'placeholder': 'Type the description',
                                          'rows': 20,
                                          'cols': 150,
                                          }
                                      ))
    price = forms.DecimalField(initial=0.00)

