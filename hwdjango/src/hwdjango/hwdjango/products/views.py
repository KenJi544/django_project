from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ProductForm
# , RawProductForm
from .models import Product
# Create your views here.


def product_table_view(request, *args, **kwargs):

    if product_sort(request):
        dictsort = product_sort(request)
    else:
        dictsort = 'id'
    queryset = Product.objects.order_by(dictsort)
    
    context = {
        'object_list': _paginate(request, queryset),
        'order': dictsort
    }
    return render(request, 'products/storage.html', context)


def _paginate(request, queryset):
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 5)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)

    return context


def product_sort(request):
    choice_list = ['id', 'title', 'description', 'price']
    if request.GET.get('sort'):
        sort = request.GET.get('sort')
        sort = str(sort.lower())
        if sort in choice_list:
            return sort
    else:
        return None


def product_detail_view(request, *args, **kwargs):
    product_id = 1
    if args:
        product_id = args[0]
    if kwargs:
        product_id = kwargs['id']

    obj = get_object_or_404(Product, id=product_id)
    context = {
            'obj': obj
            }
    return render(request, 'products/detail.html', context)


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
            'form': form
            }
    return render(request, 'products/product_create.html', context)


def product_update_view(request, *args, **kwargs):
    product_id = 1
    if args:
        product_id = args[0]
    if kwargs:
        product_id = kwargs['id']
    if request.method == 'POST':
        print('request={}'.format(request.POST.get('submit')))
    return _check_form(request, product_id)


def _check_form(request, product_id):
    obj = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=obj)
    if form.is_valid():
        context = {
            'obj': obj
        }
        form.save()
        return render(request, 'products/product_detail_view.html', context)
    context = {
            'form': form
            }
    return render(request, 'products/product_create.html', context)


def product_delete_view(request, *args, **kwargs):
    product_id = 1
    if kwargs:
        product_id = kwargs['id']

    obj = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        return _handle_post(request, obj, product_id)

    context = {
            'obj': obj
            }
    return render(request, 'products/delete.html', context)


def _handle_post(function):
        try:
            request = kwargs['request']
            obj = kwargs['instance']
            product_id = kwargs['id']
            method_get_name = kwargs['name']
        except TypeError:
            print('kwargs required: request, instance, id, name')

        def wrapper(*args, **kwargs):
            answer = str(request.POST.get(method_get_name)).lower()
            if answer != 'none':
                return function(*args, **kwargs)
            return redirect('/products/{}/'.format(product_id))
        return wrapper


@_handle_post
def _delete_function(request, obj, answer):
    if answer == 'yes':
        obj.delete()
        messages.success(request, 'Delete successfull')
        return redirect('/products/')
