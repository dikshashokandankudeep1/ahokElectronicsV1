"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from homeapp.views import Home_view, ProductList_view, ProductListOnClick_view, \
                        Product_view, ProductSearchList_view, \
                        login_View, register_View, \
                        confirmOrderDetails_View, \
                        selectDeliveryAddress_View, selectPaymentMethod_View, reviewOrderBeforePayment_View, processTopay_View,\
                        user_addToCart_View#, Admin_view, error_404, selectDeliveryAddress_View, 

from homeapp.manager import manager_default_View, manager_View
from homeapp.userAccount import account_profileInformation_View, account_View, Product_viewMore_view

#handler404 = error_404

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Home_view, name="Home_view"),
    path('login', login_View, name='login_View'),
    path('register', register_View, name='register_View'),
    #path('admin_page', Admin_view, name="Admin_view"),
    path('product-category/<str:categoryName>', ProductList_view, name="ProductList_view"),
    path('product-category/<str:categoryName>/<str:brandName>', ProductListOnClick_view, name="ProductListOnClick_view"),
    path('product/<str:modelNumber>', Product_view, name="Product_view"),
    path('product/search/<str:productTitle>', ProductSearchList_view, name="ProductSearchList_view"),

    path('product/viewMore/<str:orderId>', Product_viewMore_view, name="Product_viewMore_view"),
    #path('product/purchase', selectDeliveryAddress_View, name="selectDeliveryAddress_View"),

    #path('productAddToCart/<int:productId>', productAddToCart_View, name="productAddToCart_View"),
    #path('productRemoveFromCart/<int:productId>', productRemoveFromCart_View, name="productRemoveFromCart_View"),
    #path('clearCart', clearCart_View, name="clearCart_View"),

    #path('product/purchase/paymentGateway/<int:addressId>', confirmOrderDetails_View, name="confirmOrderDetails_View"),
    path('product/purchase/selectDeliveryAddress', selectDeliveryAddress_View, name="selectDeliveryAddress_View"),
    path('product/purchase/confirmOrderDetails', confirmOrderDetails_View, name="confirmOrderDetails_View"),
    path('product/purchase/selectPaymentMethod', selectPaymentMethod_View, name="selectPaymentMethod_View"),
    path('product/purchase/reviewOrderBeforePayment', reviewOrderBeforePayment_View, name="reviewOrderBeforePayment_View"),
    path('product/purchase/process-payment', processTopay_View, name="processTopay_View"),
    

    #path('user/<int:userID>/<int:typeofuserdatashow>', user_View, name="user_View"),       #0->profile, 1->add-to-cart, 2->orders

    path('account', account_profileInformation_View, name="account_profileInformation_View"),  #profile Information
    path('account/<str:touds>', account_View, name="account_View"),    #Manage Addresses
    #path('account/orders', orders_View, name="orders_View"),          #redirect to order page
    #path('account/<str:password>', user_View, name="user_View"),      #change password
    #path('account/<str:my-chats>', user_View, name="user_View"),      #my chat
    #path('account/<str:coupons>', user_View, name="user_View"),       #my coupons
    #path('account/<str:notifications>', user_View, name="user_View"), #my notifications
    #path('account/<str:wishlist>', user_View, name="user_View"),      #my wishlist

    path('viewcart', user_addToCart_View, name="user_addToCart_View"),     #add to cart

    path('manager', manager_default_View, name="manager_default_View"),  #profile Information
    path('manager/<str:touds>', manager_View, name="manager_View"),      #Manage Addresses

    path('manager/alterProduct/<str:touds>', manager_View, name="manager_View"),

    #path('error_404', error_404, name="error_404")
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

