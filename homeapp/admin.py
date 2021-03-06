from django.contrib import admin

from .models import  usertable, userPaymentTable, userAddressBook, userordertable, userOrderGrouptable, messagetable, \
    productsTablePrimary, productsTableSecodary, productsTableTernary, productsTableQuaterly,\
    paymentTable, promoCodes, homeSliderImageTable, homeProductListImagesTable, reviewAndRatingTable, \
    tickerTable, webCredentialsTable, temporaryOrderStoreTable, globleVariables

admin.site.register(globleVariables)
admin.site.register(usertable)
admin.site.register(userPaymentTable)
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
admin.site.register(tickerTable)
admin.site.register(webCredentialsTable)
admin.site.register(temporaryOrderStoreTable)