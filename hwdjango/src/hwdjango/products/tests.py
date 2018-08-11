from django.test import TestCase

from .forms import ProductForm


class ProductFormTest(TestCase):

    def test_form_valid(self):
        form_data = {'title': 'testitem1',
                     'price': 1}
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_false_title(self):
        form_data = {'title': '',
                     'price': 1}
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_false_price(self):
        form_data = {'title': 'testitem1',
                     'price': -1}
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
