# from django import forms
# from .models import Variation
# from django.shortcuts import get_object_or_404
# from django.shortcuts import render
# from.models import product



# class VariationInventoryForm(forms.ModelForm):
#     class Meta:
#         model = Variation
#         fields = [
#             "title",
#             "price",
#             "sale_price",
#             "inventory",
#             "active",
#         ]


# from .forms import VariationInventoryForm

# def manage_variations(request, prod_id):
#     product = get_object_or_404(product, id=prod_id)
#     form = VariationInventoryForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#     context = {
#         "form": form,
#         "product": product,
#     }
#     return render(request, "product/manage_variations.html", context)
from django import forms

class CartQuantityForm(forms.Form):
    pass