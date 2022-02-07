from django.contrib import admin

from .models import  usertable, userAddressBook, userordertable, userOrderGrouptable, messagetable, \
    productsTablePrimary, productsTableSecodary, productsTableTernary, productsTableQuaterly,\
    paymentTable, promoCodes, homeSliderImageTable, homeProductListImagesTable, reviewAndRatingTable#, hometable

#admin.site.register(hometable)
admin.site.register(usertable)
admin.site.register(userAddressBook)
admin.site.register(userordertable)
admin.site.register(userOrderGrouptable)
admin.site.register(messagetable)
admin.site.register(productsTablePrimary)
admin.site.register(productsTableSecodary)
admin.site.register(productsTableTernary)
admin.site.register(productsTableQuaterly)
admin.site.register(paymentTable)
admin.site.register(promoCodes)
admin.site.register(homeSliderImageTable)
admin.site.register(homeProductListImagesTable)
admin.site.register(reviewAndRatingTable)