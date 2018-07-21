from django.shortcuts import render

from .forms import ProductForm, RawProductForm
from .models import Product
# Create your views here.
def product_table_view(request, *args, **kwargs):
    counter = Product.objects.count()
    context_all = []
    for product_id in range(1, counter+1):
        context_all.append(product_context_generator(request, product_id))
    context_all = tuple(context_all)
    context = { 'all_products' : context_all }
    return render(request, 'products/storage.html', context)

def product_detail_view(request,*args,**kwargs):
    product_id = 1
    if args:
        product_id = args[0]
    if kwargs:
        product_id = kwargs['id']
    
    context = product_context_generator(request, id=product_id)
    return render(request, 'products/detail.html', context)

def product_context_generator(request, *args, **kwargs):
    product_id = 1
    if args:
        product_id = args[0]
    if kwargs:
        product_id = kwargs['id']

    obj = Product.objects.get(id=product_id)
    context = {
            'title' : obj.title,
            'description' : obj.description,
            'price' : obj.price
            }
    return context

#def product_create_view(request, *args, **kwargs): 
#    form = RawProductForm()
#    if request.method == "POST":
#        form = RawProductForm(request.POST)
#        if form.is_valid():
#            print(form.cleaned_data)
#            Product.objects.create(**form.cleaned_data)
#    context = {
#            'form' : form
#            }
#    return render(request, 'products/product_create.html', context)

def product_create_view(request, *args, **kwargs):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    context = {
            'form' : form
            }
    return render(request, 'products/product_create.html', context)
