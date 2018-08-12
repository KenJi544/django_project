from django.urls import path
from .views import (
    product_detail_view,
    product_table_view,
    product_create_view,
    product_update_view,
    product_delete_view,
)


app_name = 'products'
urlpatterns = [
    path('', product_table_view, name='storage'),
    path('<int:id>/', product_detail_view, name='product'),
    path('<int:id>/delete', product_delete_view, name='delete'),
    path('<int:id>/update', product_update_view, name='update'),
    path('create/', product_create_view, name='create'),
]
