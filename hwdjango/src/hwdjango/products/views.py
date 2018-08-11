from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .forms import ProductForm
# , RawProductForm
from .models import Product
# Create your views here.


class PostHandler(object):
    def __init__(self, *args):
        self.obj = args[0]

    def __call__(self, function):
        def wrapped(*args):
            result = function(*args)
            if result is None or result is False:
                return redirect('/products/{}/'.format(self.obj.pk))
            else:
                return result
        return wrapped


@login_required
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


@login_required
def product_detail_view(request, *args, **kwargs):
    try:
        product_id = kwargs['id']

        obj = get_object_or_404(Product, id=product_id)
        context = {
                'obj': obj
                }
        return render(request, 'products/detail.html', context)
    except KeyError as key_error:
        print(key_error)
        return render(request, 'products/storage.html', context)


@login_required
def product_create_view(request, *args, **kwargs):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/products/')

    context = {
            'form': form
            }
    return render(request, 'products/product_create.html', context)


@login_required
def product_update_view(request, *args, **kwargs):
    try:
        product_id = kwargs['id']
        obj = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST or None, instance=obj)

        if request.method == 'POST':
            @PostHandler(obj)
            def _update():
                tag_name = 'create'
                answer = str(request.POST.get(tag_name)).lower()
                expected = 'save'
                if answer == expected:
                    if _check_form(form):
                        messages.info(request, '{} updated'.format(obj.title))
                    else:
                        messages.info(request,
                                      "{} can't update".format(obj.title))
            return _update()
        return render(request,
                      'products/product_create.html',
                      {'form': form})
    except KeyError as key_error:
        print(key_error)


def _check_form(form):
    if form.is_valid():
        form.save()
        return True
    return False


@login_required
def product_delete_view(request, *args, **kwargs):
    try:
        product_id = kwargs['id']

        obj = get_object_or_404(Product, id=product_id)

        if request.method == 'POST':
            @PostHandler(obj)
            def _delete(**kwargs):
                tag_name = 'delete'
                answer = str(request.POST.get(tag_name)).lower()
                if answer == 'yes':
                    obj.delete()
                    messages.success(request, 'Delete successfull')
                    return redirect('/products/')
            return _delete()
        context = {
                'obj': obj
                }
        return render(request, 'products/delete.html', context)
    except KeyError as key_error:
        print(key_error)
