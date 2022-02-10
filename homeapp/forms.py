from django import forms
from .models import productsTablePrimary, productsTableTernary, homeSliderImageTable, \
                    homeProductListImagesTable

class ProductsTablePrimaryForm(forms.ModelForm):
    class Meta:
        model = productsTablePrimary
        fields = [
            'modelNumber',
            'category',
            'subCategory',
            'brandName',
            'title',
            'price',
            'quantity',
            'warranty',
            'mainImage',
            'userRatings',
            'reviewList',
        ]


class ProductsTableTernaryForm(forms.ModelForm):
    class Meta:
        model = productsTableTernary
        fields = [
            'productId',
            'hoverImage_1',
            'hoverImage_2',
            'hoverImage_3',
            'hoverImage_4',
            'hoverImage_5',
            'hoverImage_6',
        ]

class HomeSliderImageTableForm(forms.ModelForm):
    class Meta:
        model = homeSliderImageTable
        fields = [
            'image',
            'isActive',
            'productRedirectUrl',
            'description',
        ]

class HomeProductListImagesTableForm(forms.ModelForm):
    class Meta:
        model = homeProductListImagesTable
        fields = [
            'image',
            'isActive',
            'category',
            'shape'
        ]