import json, datetime

from pickle import TRUE
from threading import *
from posixpath import split
#import re
from urllib import response
from urllib import request
from urllib.request import Request
from django.contrib import messages
from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
from .models import usertable, userPaymentTable, userAddressBook, userordertable, userOrderGrouptable, \
                    homeSliderImageTable, homeProductListImagesTable,\
                    productsTablePrimary, productsTableSecodary, productsTableTernary, \
                    paymentTable, webCredentialsTable, temporaryOrderStoreTable, globleVariables, promoCodes

from django.contrib.auth.models import User, auth
from .commom import setSession, getSession, toCamelCase, toCommaSeperatedCurrency
from .threadPool import myThreadPool

from .helper import searchContentInSearchBar, checkUserLogged, getUserId, getAddToCartData, getUserName


def Home_view(request):
    print("Home_view")

    if request.method == 'POST':
        print("Home_view POST::", request.POST)

        if(request.POST.__contains__("search")):
            return searchContentInSearchBar(request)
        else:
            isNotLogged = checkUserLogged(request, request.get_full_path())
            if isNotLogged:
                return redirect(isNotLogged)

    productHomeCategoryListObj = homeProductListImagesTable.objects.filter(isActive=True)
    productHomeSliderObj       = homeSliderImageTable.objects.filter(isActive=True)

    print("productHomeCategoryListObj::", productHomeCategoryListObj)
    print("productHomeSliderObj::", productHomeSliderObj)

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}

    context = {
        'headerDict'    :   headerDict,
        'productHomeCategoryListObj'        : productHomeCategoryListObj,
        'productHomeSliderObj'              : productHomeSliderObj,
    }
    return render(request, "home/index.html", context)

def ProductList_view(request, categoryName):
    print("ProductList_view")

    if request.method == 'POST':
        print("ProductList_view request.POST::",request.POST)
        if request.POST.__contains__("search"):
            return searchContentInSearchBar(request)
        else:
            isNotLogged = checkUserLogged(request, request.get_full_path())
            if isNotLogged:
                return redirect(isNotLogged)
        
    categoryObj     =   productsTablePrimary.objects.filter(category=categoryName).filter(isActive=True)
    brandNameObj    =   categoryObj.values_list('brandName', flat=True).distinct()

    dataDict = {}
    for obj in brandNameObj:
        dataDict[obj] = categoryObj.filter(brandName=obj).count()

    print("ProductList_view dataDict::",dataDict)

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}

    context = {
        'headerDict'    :   headerDict,
        'dataDict'      : dataDict,
        'categoryName'  : categoryName,
    }
    return render(request, "product/search/countingFromTitle.html", context)



def ProductSearchList_view(request, productTitle):

    def priceFilterCalculateObj(postfilterDict, productBrandnameListObj):
        filterDictNew = dict( item.split(":") for item in postfilterDict.split(","))
        filterPriceRangeList = []
        noFilterSelected = False
        for key, value in filterDictNew.items():
            if value == '1':
                noFilterSelected = True
                filterDict[key] = 1
                vec = key.split("_")
                if vec[1] == "BL":
                    filterPriceRangeList.append((0, int(vec[2])))
                elif vec[1] == "BTW":
                    filterPriceRangeList.append((int(vec[2]), int(vec[3])))
                elif vec[1] == "ABW":
                    filterPriceRangeList.append((int(vec[2]), 99999999))
                else:
                    print("ERROR:: at POST FILTER:PRICE", vec)
            else:
                filterDict[key] = 0

        tempUsertableObjMain = usertable.objects.none()

        for data in filterPriceRangeList:
            tempUsertableObjMain |= productBrandnameListObj.filter(
                    price__range=(data[0], data[1])
                )

        if tempUsertableObjMain.exists() or noFilterSelected:
            return tempUsertableObjMain
        else:
            return productBrandnameListObj


    print("ProductSearchList_view START::", productTitle)
    
    productproductTitleListObj = productsTablePrimary.objects.filter(searchTitle__contains=productTitle.replace(" ", "").lower()).filter(isActive=True)
    filterDict = {"PRICE_BL_2000" : 0, "PRICE_BTW_2000_3000" : 0, "PRICE_BTW_3000_4000" : 0, "PRICE_BTW_4000_5000" : 0, "PRICE_ABW_5000" : 0}
    SORTBY = 'Popularity'

    url = ""
    if request.method == 'POST':
        print("ProductSearchList_view POST::", request.POST)
        if(request.POST.__contains__("search")):
            return searchContentInSearchBar(request)
        elif(request.POST.__contains__("FILTER:PRICE")):
            productproductTitleListObj = priceFilterCalculateObj(request.POST["filterDict"], productproductTitleListObj)
            
        elif(request.POST.__contains__("dropdownSortButton")):
            SORTBY = request.POST["dropdownSortButton"]
            productproductTitleListObj = priceFilterCalculateObj(request.POST["dropdownSortButtonfilterDict"], productproductTitleListObj)
            #todo handle other sort methods Newsest, Popularity --> currntly taken High to Low
            if request.POST["dropdownSortButton"] == "LTH":
                productproductTitleListObj = productproductTitleListObj.order_by('price')
            else:
                productproductTitleListObj = productproductTitleListObj.order_by('-price')

    print("ProductSearchList_view productTitle::",productTitle)

    relaventContent = ""
    isSearchContentFound = ""
    if productproductTitleListObj.count() == 0:
        isSearchContentFound = 0
        relaventContent = 'Red Mi'  #todo user old history search based data
        productproductTitleListObj  =  productsTablePrimary.objects.filter(searchTitle__contains=relaventContent.replace(" ", "").lower())
    else:
        isSearchContentFound = 1

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
        'headerDict'    :   headerDict,
        'searchContent'     :   productTitle,
        'isSearchContentFound' : isSearchContentFound,
        'relaventContent'    :  relaventContent,
        'filterDict'        :   filterDict,
        'SORTBY'        :   SORTBY,
        'searchTitle'   :   productTitle,
        'productBrandnameListObj'        : productproductTitleListObj,
        'productBrandnameListObjCount'   : productproductTitleListObj.count(),
        'categoryName'                   : "",
        'brandName'                      : ""
    }
    return render(request, "product/search/fromTitle.html", context)


def fillTemporaryOrderStoreTable(userId, deleveryAddressId, selectedMode, paymentModeId, currentOrderList):
    temporaryOrderStoreTableObj = temporaryOrderStoreTable.objects.filter(userId=userId)
    if len(temporaryOrderStoreTableObj) == 0:
        obj = temporaryOrderStoreTable(userId=userId, deleveryAddressId=deleveryAddressId, 
            selectedMode=selectedMode, paymentModeId=paymentModeId, currentOrderList=currentOrderList)
        obj.save()
    else:
        for obj in temporaryOrderStoreTableObj:
            if deleveryAddressId:
                if deleveryAddressId == "clear":
                    obj.deleveryAddressId = ""
                else:   
                    obj.deleveryAddressId = deleveryAddressId
            if selectedMode:
                if selectedMode == "clear":
                    obj.selectedMode = ""
                else:   
                    obj.selectedMode = selectedMode
            if paymentModeId:
                if paymentModeId == "clear":
                    obj.paymentModeId = ""
                else:   
                    obj.paymentModeId = paymentModeId
            if currentOrderList:
                if currentOrderList == "clear":
                    obj.currentOrderList = ""
                else:   
                    obj.currentOrderList = currentOrderList
            obj.save()
    return

def getTemporaryOrderStoreTable(userId, deleveryAddressId, selectedMode, paymentModeId, currentOrderList):
    temporaryOrderStoreTableObj = temporaryOrderStoreTable.objects.filter(userId=userId)
    if len(temporaryOrderStoreTableObj) == 0:
        print("ERROR:: occurs when getTemporaryOrderStoreTable object length check")
        return ""
    else:
        for obj in temporaryOrderStoreTableObj:
            if deleveryAddressId:
                return obj.deleveryAddressId
            if selectedMode:
                return obj.selectedMode
            if paymentModeId:
                return obj.paymentModeId
            if currentOrderList:
                return obj.currentOrderList

def ProductListOnClick_view(request, categoryName, brandName):

    def priceFilterCalculateObj(postfilterDict, productBrandnameListObj):
        filterDictNew = dict( item.split(":") for item in postfilterDict.split(","))
        filterPriceRangeList = []
        noFilterSelected = False
        for key, value in filterDictNew.items():
            if value == '1':
                noFilterSelected = True
                filterDict[key] = 1
                vec = key.split("_")
                if vec[1] == "BL":
                    filterPriceRangeList.append((0, int(vec[2])))
                elif vec[1] == "BTW":
                    filterPriceRangeList.append((int(vec[2]), int(vec[3])))
                elif vec[1] == "ABW":
                    filterPriceRangeList.append((int(vec[2]), 99999999))
                else:
                    print("ERROR:: at POST FILTER:PRICE", vec)
            else:
                filterDict[key] = 0

        tempUsertableObjMain = usertable.objects.none()

        for data in filterPriceRangeList:
            tempUsertableObjMain |= productBrandnameListObj.filter(
                    price__range=(data[0], data[1])
                )

        if tempUsertableObjMain.exists() or noFilterSelected:
            return tempUsertableObjMain
        else:
            return productBrandnameListObj


    print("ProductListOnClick_view request.user.id::", request.user.id)
    
    productBrandnameListObj = productsTablePrimary.objects.filter(category=categoryName).filter(brandName=brandName).filter(isActive=True)
    print("----------------", productBrandnameListObj.values())
    filterDict = {"PRICE_BL_2000" : 0, "PRICE_BTW_2000_3000" : 0, "PRICE_BTW_3000_4000" : 0, "PRICE_BTW_4000_5000" : 0, "PRICE_ABW_5000" : 0}
    SORTBY = 'Popularity'

    if request.method == 'POST':
        print("ProductListOnClick_view POST::", request.POST)
        updateaddToCartID = ""
        url = ""
        if request.POST.__contains__("ADDTOCART") or request.POST.__contains__("BUYNOW"):
            print("request.user.id::",request.user.id)
            isNotLogged = checkUserLogged(request, request.get_full_path())
            if isNotLogged:
                return redirect(isNotLogged)
            
            if request.POST.__contains__("ADDTOCART"):
                print("ProductListOnClick_view request.POST['ADDTOCART']::", request.POST['ADDTOCART'])
                updateaddToCartID = request.POST['ADDTOCART']
                url = "/viewcart"
            elif request.POST.__contains__("BUYNOW"):
                print("ProductListOnClick_view request.POST['BUYNOW']::", request.POST['BUYNOW'])
                updateaddToCartID = request.POST['BUYNOW']
                url = "/product/purchase/selectDeliveryAddress"
                fillTemporaryOrderStoreTable(request.user.id, "", "", "", [updateaddToCartID])
             
        elif(request.POST.__contains__("search")):
            print("ProductListOnClick_view searchContent")
            return searchContentInSearchBar(request)
        elif(request.POST.__contains__("FILTER:PRICE")):
            print("ProductListOnClick_view FILTER:PRICE::",request.POST["FILTER:PRICE"])
            productBrandnameListObj = priceFilterCalculateObj(request.POST["filterDict"], productBrandnameListObj)
            print("ProductListOnClick_view productBrandnameListObj::",productBrandnameListObj)

        elif(request.POST.__contains__("dropdownSortButton")):
            print("ProductListOnClick_view dropdownSortButton::",request.POST["dropdownSortButton"])
            SORTBY = request.POST["dropdownSortButton"]
            productBrandnameListObj = priceFilterCalculateObj(request.POST["dropdownSortButtonfilterDict"], productBrandnameListObj)
            print("productBrandnameListObj::",productBrandnameListObj)
            if request.POST["dropdownSortButton"] == "LTH":
                productBrandnameListObj = productBrandnameListObj.order_by('price')
            else:
                productBrandnameListObj = productBrandnameListObj.order_by('-price')
        else:
            print("ProductListOnClick_view some other case")

        addToCartItemsDict = {}
        if updateaddToCartID != "":
            userObject = usertable.objects.filter(userId=request.user.id)[0]
            print("ProductListOnClick_view POST userObject::", userObject)
            if userObject.addToCartItemsDict != "":
                print("ProductListOnClick_view userObject.addToCartItemsDict::",userObject.addToCartItemsDict)
                addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))
                print("addToCartItemsDict::", addToCartItemsDict)
                if addToCartItemsDict.__contains__(updateaddToCartID):
                    addToCartItemsDict[updateaddToCartID] += 1
                else:
                    addToCartItemsDict[updateaddToCartID] = 1
            else:
                addToCartItemsDict[updateaddToCartID] = 1

            userObject.addToCartItemsDict = str(addToCartItemsDict)
            userObject.save()
            print("ProductListOnClick_view POST =============== userObject.addToCartItemsDict::", userObject.addToCartItemsDict)
        print("ProductListOnClick_view url::", url)

        if url and url != "/viewcart":
            return redirect(url)
    else:
        #todo if any error came
        print("Method is GET Bada dikkat he re deva....")

    print("ProductListOnClick_view 3 productBrandnameListObj::",productBrandnameListObj)
    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}

    context = {
        'headerDict'                     : headerDict,
        'searchTitle'                    : "",
        'productBrandnameListObj'        : productBrandnameListObj,
        'productBrandnameListObjCount'   : productBrandnameListObj.count(),
        'categoryName'                   : categoryName,
        'brandName'                      : brandName,
        'filterDict'        :   filterDict,
        'SORTBY'            :   SORTBY,
        'searchContent'     :   brandName,
    }
    return render(request, "product/search/fromTitle.html", context)


def Product_view(request, modelNumber):

    print("Product_view::", request, " | ", modelNumber)

    if request.method == 'POST':
        print("Product_view POST")

        if(request.POST.__contains__("search")):
            return searchContentInSearchBar(request)
        else:
            isNotLogged = checkUserLogged(request, request.get_full_path())
            if isNotLogged:
                return redirect(isNotLogged)
        
        url = ""
        updateaddToCartID = ""
        
        print("Product_view 1 POST request.POST::",request.POST)
        if(request.POST.__contains__("ADDTOCART")):
            updateaddToCartID = request.POST['ADDTOCART']
            url = "/viewcart"
        else:
            print("Product_view request.POST['BUYNOW']::", request.POST['BUYNOW'])
            updateaddToCartID = request.POST['BUYNOW']
            url = "/product/purchase/selectDeliveryAddress"
            fillTemporaryOrderStoreTable(request.user.id, "", "", "", [updateaddToCartID])
            #setSession(request, 'currentOrderList', [updateaddToCartID])
           
        userObject = usertable.objects.filter(userId=request.user.id)[0]
        print("Product_view POST userObject::", userObject)

        addToCartItemsDict = {}
        if userObject.addToCartItemsDict != "":
            addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))

        print("Product_view POST addToCartItemsDict::", addToCartItemsDict)
        if addToCartItemsDict.__contains__(updateaddToCartID):
            addToCartItemsDict[updateaddToCartID] += 1
        else:
            addToCartItemsDict[updateaddToCartID] = 1

        userObject.addToCartItemsDict = str(addToCartItemsDict)
        userObject.save()

        print("Product_view url::", url)
        if url and url != "/viewcart":
            return redirect(url)
    
    HoverImageDict = {}
    HoverImageDict[1] = productsTablePrimary.objects.filter(modelNumber=modelNumber)[0].mainImage.url
    objTernary = productsTableTernary.objects.filter(productId=modelNumber)
    print("Product_view 1 modelNumber::",modelNumber, objTernary)

    if len(objTernary):
        HoverImageDict = objTernary[0].getHoverImageDict()

    print("Product_view 6::")
    dataData = {
        "HoverImageDict"  : HoverImageDict,
        "Highlight" : {},
        "Spacification" : {}
    }
    if productsTableSecodary.objects.filter(productId=modelNumber).exists():
        for key, value in productsTableSecodary.objects.filter(productId=modelNumber).values()[0].items():
            if key != 'id' and key != 'productId' and value:
                value = value.split("|")
                dataData["Highlight"][value[0]] = value[1]  #todo
    
    print("Product_view 8::")
    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
        'headerDict'    :   headerDict,
        'instance'      :   productsTablePrimary.objects.filter(modelNumber=modelNumber)[0],
        'dataData'      :   dataData
    }
    return render(request, "product/detail.html", context)

def user_addToCart_View(request):

    dataDictionary = {}
    userObject = usertable.objects.filter(userId=request.user.id)
    if len(userObject) == 0:
        context = {"url" : request.get_full_path()}
        return render(request,"404.html", context)
    else:
        userObject = userObject[0]

    print("user_addToCart_View 0 userObject::", userObject)

    flgCHANGEDQUANTITY = False
    if request.method =="POST":
        print("user_addToCart_View 0 request.POST", request.POST)
        if request.POST.__contains__("PROCEEDTOBUYFORM"):
            addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))
            addToCartKeys = list(addToCartItemsDict.keys())
            notPurchasedItemList = []
            print('request.POST["PROCEEDTOBUYFORM"]::', request.POST["PROCEEDTOBUYFORM"])
            if request.POST["PROCEEDTOBUYFORM"] !="[]":
                notPurchasedItemList = request.POST["PROCEEDTOBUYFORM"].strip("[]").split(",")
            outputList = list(set(addToCartKeys) - set(notPurchasedItemList)) + list(set(notPurchasedItemList) - set(addToCartKeys))
            fillTemporaryOrderStoreTable(request.user.id, "", "", "", outputList)
            print("user_addToCart_View currentOrderList::", getTemporaryOrderStoreTable(request.user.id, 0, 0, 0, 1))
            return redirect("/product/purchase/selectDeliveryAddress")
        elif request.POST.__contains__("CHANGEDQUANTITY"):
            flgCHANGEDQUANTITY = True

        elif(request.POST.__contains__("search")):
            print("ProductListOnClick_view searchContent")
            return searchContentInSearchBar(request)

    print("user_addToCart_View 1 add-to-cart userObject.addToCartItemsDict::",userObject.addToCartItemsDict)
    addToCartItemsDict = {}
    if (userObject.addToCartItemsDict) !="" and (userObject.addToCartItemsDict != '{}'):
        print("user_addToCart_View 1 add-to-cart IF")
        addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))
        productDictList = []
        itemidList  =  []
        subtotal = 0
        totalQuantity = 0
        print("user_addToCart_View 1 request.POST",request.POST)
        if flgCHANGEDQUANTITY:
            if addToCartItemsDict.__contains__(request.POST["ITEMID"]):
                itemID       = request.POST["ITEMID"]
                itemQuantity = addToCartItemsDict[itemID]

                if request.POST["CHANGEDQUANTITY"] =="0":
                    del addToCartItemsDict[itemID]
                else:
                    itemQuantity = int(request.POST['CHANGEDQUANTITY'])
                    addToCartItemsDict[itemID] =  itemQuantity

                if addToCartItemsDict == {}:
                    userObject.addToCartItemsDict =""
                else:
                    userObject.addToCartItemsDict = str(addToCartItemsDict)
                userObject.save()
            else:
                print("ERROR::user_addToCart_View 1 addToCartItemsDict does not have CHANGEDQUANTITY")
        for itemID, itemQuantity in addToCartItemsDict.items():
            productObjs = productsTablePrimary.objects.filter(modelNumber=itemID)
            for productObj in productObjs:
                productDictList.append({ "itemID" : itemID, "title" : productObj.title, 
                                        "price" : toCommaSeperatedCurrency(productObj.price), 
                                        "imageurl": productObj.mainImage.url, 
                                        "quantity" : itemQuantity, "storeQuantity" : productObj.quantity } )
                itemidList.append(itemID)
                totalQuantity += itemQuantity
                subtotal += (productObj.price * itemQuantity)
            else:
                #TODO << Item out of stock >>
                print("WE have issue at productPaymentGateway productObj...", len(productObjs))

        dataDictionary = {"productDictList" : productDictList, "itemidList" : itemidList,
                            "totalQuantity" : totalQuantity, "subtotal" : toCommaSeperatedCurrency(subtotal)}
    else:
        print("user_addToCart_View 1 add-to-cart ELSE")
        dataDictionary = {"productDictList" : [], "itemidList" : [],"totalQuantity": 0,"subtotal" : 0}

    print("user_addToCart_View 2 dataDictionary::", dataDictionary)
    
    if dataDictionary["productDictList"] == []:
        return redirect("/")

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
       'headerDict'    :   headerDict,
       "dataDictionary"      : dataDictionary
    }
    return render(request,"user/addToCart/index.html", context)

def selectDeliveryAddress_View(request):
    
    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    print("selectDeliveryAddress_View")
    userAddressBookList = []
    userAddressBookItemDelete = ""
    userAddressBookItemEditObj = ""

    userObjects = usertable.objects.filter(userId=request.user.id)
    print("selectDeliveryAddress_View userObjects::", userObjects)

    if request.method == 'POST':
        print("request POST::",request.POST)
        print("request POST userObjects::",userObjects)

        if "EDIT" in request.POST.keys() or "DELETE" in request.POST.keys():
            print("selectDeliveryAddress_View Address EDIT or DELETE")
            if "EDIT" in request.POST.keys() and request.POST['EDIT'] != "":
                userAddressBookItemEditObj = userAddressBook.objects.filter(id=int(request.POST['EDIT']))[0]
            elif request.POST['DELETE'] != "":
                userAddressBookItemDelete = int(request.POST['DELETE'])
        elif "DELIVERYADDRESS" in request.POST.keys():
            fillTemporaryOrderStoreTable(request.user.id, request.POST['DELIVERYADDRESS'], "", "", "")
            #setSession(request, 'deleveryAddressId', int(request.POST['DELIVERYADDRESS']))
            return redirect("/product/purchase/confirmOrderDetails")
        else:
            print("selectDeliveryAddress_View Address alter")
            firstName       = toCamelCase(request.POST['firstName'])
            lastName        = toCamelCase(request.POST['lastName'])
            locationType    = toCamelCase(request.POST['locationType'])
            country         = toCamelCase(request.POST['country'])
            address         = toCamelCase(request.POST['address'])
            landmark        = toCamelCase(request.POST['landmark'])
            townOrCity      = toCamelCase(request.POST['townOrCity'])
            state           = toCamelCase(request.POST['state'])
            postcodeOrZIP   = request.POST['postcodeOrZIP']
            phoneNo         = request.POST['phoneNo']
            emailAddress    = request.POST['emailAddress']
            orderNotes      = request.POST['orderNotes']

            print("selectDeliveryAddress_View 1")

            if "MODIFYADDRESS" not in request.POST.keys():
                print("selectDeliveryAddress_View address:: Add new address")
                userAddressBook_ = userAddressBook(userId=request.user.id, firstName=firstName, lastName=lastName, locationType=locationType,
                                        country=country, address=address, landmark=landmark,
                                        townOrCity=townOrCity, state=state, postcodeOrZIP=postcodeOrZIP, phoneNo=phoneNo,
                                        emailAddress=emailAddress, orderNotes=orderNotes)
                userAddressBook_.save()

                for obj in userObjects:
                    if (obj.userAddressBooks != "") and (obj.userAddressBooks != "[]"):
                        userAddressBookList = list(map(int, obj.userAddressBooks.strip('][').split(', ')))
                        userAddressBookList.append(userAddressBook_.id)
                        obj.userAddressBooks = str(userAddressBookList)
                        print("obj.userAddressBooks if::", obj.userAddressBooks)
                    else:
                        obj.userAddressBooks = str([userAddressBook_.id])
                        userAddressBookList = [userAddressBook_.id]
                        print("obj.userAddressBooks else::", obj.userAddressBooks)
                    obj.save()
            else:
                print("selectDeliveryAddress_View Address Modify")
                userAddressBook_ = userAddressBook(id=int(request.POST['MODIFYADDRESS']), userId=request.user.id, firstName=firstName, 
                                        lastName=lastName, locationType=locationType,
                                        country=country, address=address, landmark=landmark,
                                        townOrCity=townOrCity, state=state, postcodeOrZIP=postcodeOrZIP, phoneNo=phoneNo,
                                        emailAddress=emailAddress, orderNotes=orderNotes)
                userAddressBook_.save()

        print("selectDeliveryAddress_View ListOfAddress_1::create userAddressBookList for list of address")
        for obj in userObjects:
            print("obj::",obj)
            print("obj.userAddressBooks::",obj.userAddressBooks)
            if obj.userAddressBooks and obj.userAddressBooks != "[]":
                if not userAddressBookItemEditObj:
                    userAddressBookList = list(map(int, obj.userAddressBooks.strip('][').split(', ')))
                if userAddressBookItemDelete:
                    print("userAddressBookList, userAddressBookItemDelete::", userAddressBookList, userAddressBookItemDelete)
                    userAddressBookList.remove(userAddressBookItemDelete)
                    userAddressBookItemDelete = ""
                    obj.userAddressBooks = str(userAddressBookList)
                    obj.save()
        print("userAddressBookList::",userAddressBookList)
    else:
        #todo GET METHOD
        print("selectDeliveryAddress_View GET METHOD :: show user all list of address on top of page")
        for obj in userObjects:
            print("ELSE obj.userAddressBooks::", obj.userAddressBooks)
            if (obj.userAddressBooks != "") and (obj.userAddressBooks != "[]"):
                userAddressBookList = list(map(int, obj.userAddressBooks.strip('][').split(', ')))

    userAddressBookDictList = []
    if userAddressBookList != []:
        print("selectDeliveryAddress_View ListOfAddress_2::create userAddressBookList for list of address")
        for idData in userAddressBookList:
            useraddressBookObj = userAddressBook.objects.filter(id=idData)
            if len(useraddressBookObj) == 1:
                useraddressBookObj = useraddressBookObj[0]
                dataDict = {}
                dataDict["id"] = idData
                dataDict["userFullName"]    = useraddressBookObj.firstName + " " + useraddressBookObj.lastName
                dataDict["address"]         = useraddressBookObj.address
                dataDict["landmark"]        = useraddressBookObj.landmark
                dataDict["townCity"]        = useraddressBookObj.townOrCity + ", " + useraddressBookObj.state  +\
                                                 " " + useraddressBookObj.postcodeOrZIP
                dataDict["country"]         = useraddressBookObj.country
                dataDict["phoneNo"]         = useraddressBookObj.phoneNo
                dataDict["orderNotes"]      = useraddressBookObj.orderNotes
                userAddressBookDictList.append(dataDict)
            else:
                print("WE have issue at selectDeliveryAddress_View ListOfAddress_2...", len(useraddressBookObj))

    print("selectDeliveryAddress_View END")

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}

    context = {
        'headerDict'                    :   headerDict,
        "userAddressBookDictList"       :   userAddressBookDictList,
        "userAddressBookDictListCount"  :   len(userAddressBookDictList),
        "userAddressBookItemEditObj"    :   userAddressBookItemEditObj
    }
    return render(request, "product/purchase/selectAddress/index.html", context)

def placeOrderInit(request, userObject, orderDeliveryAddress, onOrderPaidAmount, orderFirstPaidTrxnID, orderFirstPaymentID):
    userOrderGrouptable_ = userOrderGrouptable(userId=request.user.id, ordersList="")
    typeofpayment = False
    if request.POST['TYPEOFPAYMENT'] == "PARTIAL":
        typeofpayment = False
    else:
        typeofpayment = True

    addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))

    orderTableIdList = []
    currentOrderList = getTemporaryOrderStoreTable(request.user.id, 0, 0, 0, 1)
    for itemID, itemQuantity in addToCartItemsDict.items():
        if currentOrderList:
            if not (itemID in currentOrderList):
                continue
        #if request.session.__contains__("currentOrderList"):
            #if not (itemID in getSession(request, "currentOrderList")):
                #continue
        productObjs = productsTablePrimary.objects.filter(modelNumber=itemID)
        for productObj in productObjs:
            print("placeOrderInit userordertable started for ::", itemID)
            #-------------Discount and Extra Delivey changes---STARTED-----------
            orderTotalDiscountPercentage = 0;   #todo Discount
            orderDeliveryCharge = 0;   #todo delivery charge
            if not orderTotalDiscountPercentage:
                finalPaidAmount = (productObj.price * itemQuantity)  +  orderDeliveryCharge
            else:
                finalPaidAmount = (productObj.price * itemQuantity) *  (orderTotalDiscountPercentage / 100)  +  orderDeliveryCharge
            #-------------Discount and Extra Delivey changes---END-----------
            userordertable_ = userordertable( userId=request.user.id, orderDeliveryAddress=orderDeliveryAddress, orderId="",
                                typeofpayment=typeofpayment, orderFirstPaidTrxnID=orderFirstPaidTrxnID, orderSecondPaidTrxnID='',
                                orderFirstPaymentID=orderFirstPaymentID, orderSecondPaymentID='',
                                orderPlacedDate=datetime.datetime.now(), orderEstimatedArrivalDateStart=datetime.datetime.now(),
                                orderEstimatedArrivalDateEnd=datetime.datetime.now(), orderFirstPaymentDate=datetime.datetime.now(),
                                orderSecondPaymentDate=datetime.datetime.now(), orderItemId=itemID, orderTitle=productObj.title,
                                orderedItemImage=productObj.mainImage,  orderSellingPricePerItem=productObj.price,
                                orderSellingQuantity=itemQuantity,  onOrderPaidAmount=onOrderPaidAmount,
                                paidAmount=onOrderPaidAmount, finalPaidAmount=finalPaidAmount,
                                orderDeliveryCharge=orderDeliveryCharge, orderDiscountCouponId=0, orderTrackingStatus=0)
            userordertable_.save()
            orderTableIdList.append(userordertable_.id)
            print("placeOrderInit userordertable END for ::", itemID)
            productObj.quantity -= itemQuantity
            productObj.save()
        
    userOrderGrouptable_.ordersList = str(orderTableIdList)
    userOrderGrouptable_.save()

    print("placeOrderInit userOrderGrouptable::", userOrderGrouptable_)

    for id in orderTableIdList:
        userordertable_ = userordertable.objects.filter(id=id)[0]
        userordertable_.orderId = str(request.user.id) + "-" + str(userOrderGrouptable_.id) + "-" + str(userordertable_.id)
        userordertable_.save()

    print("placeOrderInit orderId updated in userordertable")

    currentOrderList = getTemporaryOrderStoreTable(request.user.id, 0, 0, 0, 1)
    if currentOrderList:
        for itemID in currentOrderList:
            del addToCartItemsDict[itemID]
        fillTemporaryOrderStoreTable(request.user.id, "", "", "", "clear")

    #if request.session.__contains__("currentOrderList"):
    #    for itemID in getSession(request, "currentOrderList"):
    #        del addToCartItemsDict[itemID]
    #    del request.session["currentOrderList"]

    if addToCartItemsDict == {}:
        userObject.addToCartItemsDict = ""
    else:
        userObject.addToCartItemsDict = str(addToCartItemsDict)

    userObject.save()


def confirmOrderDetails_View(request):
    
    print("confirmOrderDetails_View...")

    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    userObject = usertable.objects.filter(userId=request.user.id)[0]
    print("confirmOrderDetails_View start userObject::", userObject)

    if userObject.addToCartItemsDict != "":
        print("userObject.addToCartItemsDict::", userObject.addToCartItemsDict)
        addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))
    orderDeliveryAddress = ""

    if request.method == 'POST':
        if request.POST.__contains__("CHANGEDQUANTITY"): #click on update button after change quantity
            print("confirmOrderDetails_View click on update button request.POST", request.POST)
            updateditemquantity = ""
            updateditemID = ""
            orderDeliveryAddress    = request.POST["DELIVERYADDRESS"]
            updateditemquantity     = int(request.POST["CHANGEDQUANTITY"])
            updateditemID           = request.POST["ITEMID"]

            if updateditemquantity != 0:
                addToCartItemsDict[updateditemID] = updateditemquantity
                print("confirmOrderDetails_View 1 if updateditemquantity::", updateditemquantity)
            else:
                del addToCartItemsDict[updateditemID]
                print("confirmOrderDetails_View 1 else updateditemquantity::", updateditemquantity)

            if addToCartItemsDict == {}:
                userObject.addToCartItemsDict = ""
            else:
                userObject.addToCartItemsDict = str(addToCartItemsDict)
            userObject.save()
        elif request.POST.__contains__("buttonOpeartion"):
            if request.POST["buttonOpeartion"] == "cancel":
                return redirect("/")
            else:#submit
                fillTemporaryOrderStoreTable(request.user.id, "", request.POST["selectedMode"], "", "") #token or full
                return redirect("/product/purchase/selectPaymentMethod")
        else: #when click on Place Order after payment contain ORDERFIRSTTRXNID
            print("confirmOrderDetails_View Place order button click request.POST", request.POST)
            orderDeliveryAddress        = request.POST["DELIVERYADDRESS"]
            onOrderPaidAmount           = request.POST["onOrderPaidAmount"]
            orderFirstPaidTrxnID        = request.POST['ORDERFIRSTTRXNID']
            orderFirstPaymentID         = request.POST['PAYMENTID']

            placeOrderInit(request, userObject, orderDeliveryAddress, onOrderPaidAmount, orderFirstPaidTrxnID, orderFirstPaymentID)
            
            url = "/account/orders"

            print("confirmOrderDetails_View 1 else url::", url)

            return redirect(url)

    if orderDeliveryAddress == "":
        addressId = getTemporaryOrderStoreTable(request.user.id, 1, 0, 0, 0)
        useraddressBookObj = userAddressBook.objects.filter(id=addressId)
        for obj in useraddressBookObj:
            orderDeliveryAddress =  obj.firstName + " " \
                                + obj.lastName + ", " \
                                + obj.address + ", " \
                                + obj.landmark + ", " \
                                + obj.townOrCity + ", " \
                                + obj.state  + " " \
                                + obj.postcodeOrZIP + ", " \
                                + obj.country + ", " \
                                + "Contact No." + obj.phoneNo

            print("orderDeliveryAddress: ", orderDeliveryAddress)
        else:
            print("WE have issue at productPaymentGateway useraddressBookObj...", len(useraddressBookObj))

    print("confirmOrderDetails_View 4 addToCartItemsDict::", addToCartItemsDict)
    print("request.session['currentOrderList']::", getTemporaryOrderStoreTable(request.user.id, 0, 0, 0, 1))
    
    productDictList = []
    productsTotalCost = 0
    tokenAmount = 0
    itemidList  =  []

    currentOrderList = getTemporaryOrderStoreTable(request.user.id, 0, 0, 0, 1)
    for itemID, itemQuantity in addToCartItemsDict.items():
        if currentOrderList:
            if not (itemID in currentOrderList):
                continue
        
        tokenPercentage = 20
        minimumTotalCost = 1000
        glbObj = globleVariables.objects.all()
        for objData in glbObj:
            tokenPercentage = objData.tokenPercentage
            minimumTotalCost = objData.minimumTotalCost

        productObj = productsTablePrimary.objects.filter(modelNumber=itemID)
        for obj in productObj:
            productDictList.append({ "itemID" : itemID, "title" : obj.title, "price" : obj.price, "quantity" : itemQuantity, "storeQuantity": obj.quantity})
            productTotalCost = obj.price * itemQuantity
            productsTotalCost += productTotalCost
            tokenAmount += productTotalCost * (tokenPercentage/100)
            itemidList.append(itemID)

        if len(productObj) != 1:
            #TODO << Item out of stock >>
            print("WE have issue at productPaymentGateway productObj...", len(productObj))

    print("itemidList::", itemidList)
    if(len(itemidList) == 0):
        return redirect("/")
    
    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
        'headerDict'                :   headerDict,
        "orderDeliveryAddress"      : orderDeliveryAddress,
        "productDictList"           : productDictList,
        "itemidList"                : itemidList,
        "productsTotalCost"         : productsTotalCost,
        "minimumTotalCost"          : minimumTotalCost,
        "tokenAmount"               : round(tokenAmount),
    }

    return render(request, "product/purchase/deleveryDetailsConfirmation.html", context)
    

def selectPaymentMethod_View(request):

    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    if request.method == 'POST':
        print("selectPaymentMethod_View POST::", request.POST)
        if request.POST['buttonOpeartion'] == "cancel":
            redirect("/")
        elif request.POST['methodOfPayment'] == 'upi':
            tempObj = temporaryOrderStoreTable.objects.filter(userId=request.user.id)
            for obj in tempObj:
                obj.paymentModeId = "upi"
                obj.cvvOrUpi = request.POST['cvvOrUpi']
                obj.save()

            return redirect("/product/purchase/reviewOrderBeforePayment")

        elif request.POST['methodOfPayment'] == 'acc':
            tempObj = temporaryOrderStoreTable.objects.filter(userId=request.user.id)
            for obj in tempObj:
                obj.paymentModeId = "acc"
                obj.cvvOrUpi = request.POST['cvvOrUpi']
                obj.accId = request.POST['accId']
                obj.save()

            return redirect("/product/purchase/reviewOrderBeforePayment")

        elif request.POST['methodOfPayment'] == 'addACard':
            cardNumber = request.POST['formCardNumber']
            cardHolderName = request.POST['formNameOnCard'].replace(" ", "").upper()
            expiryDate = request.POST['formExpiryDate']
            bankName = toCamelCase(request.POST['formBankName'])
            cardType = toCamelCase(request.POST['formCardType'])
            cardObj = userPaymentTable(userId=request.user.id, cardNumber=cardNumber, cardHolderName=cardHolderName, 
                            expiryDate=expiryDate, bankName=bankName, cardType=cardType)
            cardObj.save()
            cardObj.id = int(cardObj.id)
            userObj = usertable.objects.filter(userId=request.user.id)
            for obj in userObj:
                if not obj.accountList :
                    obj.accountList = [ cardObj.id ]
                else:
                    accountList = obj.accountList
                    accountList = [ int(item) for item in  accountList.replace("[", "").replace("]", "").split(", ") ]
                    if not cardObj.id in accountList:
                        accountList.append(cardObj.id)
                        obj.accountList = str(accountList)
                obj.save()
            
    accIds = []
    userObj = usertable.objects.filter(userId=request.user.id)
    
    for obj in userObj:
        print("selectPaymentMethod_View obj.accountList::", obj.accountList)
        if obj.accountList:
            accIds = [ str(item) for item in  obj.accountList.replace("[", "").replace("]", "").split(", ") ]

    cardsDict = {}
    userCardObj = userPaymentTable.objects.filter(userId=request.user.id)
    for obj in userCardObj:
        data = {}
        data["cardNumber"]      = obj.cardNumber[-4:]
        data["cardHolderName"]  = obj.cardHolderName
        data["expiryDate"]      = obj.expiryDate
        data["bankName"]        = obj.bankName
        data["cardType"]        = obj.cardType
        cardsDict[obj.id] = data
    
    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}

    context = {
        'headerDict'    :   headerDict,
        'accIds'    :   accIds,
        'accIdsCount' : len(accIds),
        'cardsDict' :   cardsDict
    }
    return render(request, "product/purchase/selectPaymentMethod.html", context)

def reviewOrderBeforePayment_View(request):

    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    isPromoCodeWrong = 0
    isPromoCodeNotEntered = 1
    discountPercentage = 0
    
    if request.method == 'POST':
        if request.POST.__contains__("buttonOpeartion"):
            print("buttonOpeartion::", request.POST["buttonOpeartion"])
            if request.POST["buttonOpeartion"] == "submit":
                return redirect("/product/purchase/process-payment")
            else:
                return redirect("/")
                
        elif request.POST.__contains__("promoCode"):
            promoObj = promoCodes.objects.filter(promoCodeId=request.POST["promoCode"].lower())
            if promoObj:
                discountPercentage = promoObj[0].discountPercentage
                isPromoCodeNotEntered = 0
            else:
                isPromoCodeWrong = 1
                
        elif request.POST.__contains__("reEnterPromoCode"):
            pass
    
    dataDict = {}
    dataDict['isPromoCodeNotEntered'] = isPromoCodeNotEntered
    tempObj = temporaryOrderStoreTable.objects.filter(userId=request.user.id)
    for obj in tempObj:

        orderSummery = {}
        tokenPercentage = 20
        deliveryChargePercentage = 0
        glbObj = globleVariables.objects.all()
        for objData in glbObj:
            tokenPercentage = objData.tokenPercentage
            deliveryChargePercentage = objData.deliveryChargePercentage
        
        productsTotalCost = 0
        tokenAmount = 0
        totalItemQuantity = 0
        promoDiscount = 0
        deliveryCharge = 0

        userObject = usertable.objects.filter(userId=request.user.id)
        for userObj in userObject:
            addToCartItemsDict = {}
            addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObj.addToCartItemsDict.strip('}{').split(","))
            for itemID, itemQuantity in addToCartItemsDict.items():
                if obj.currentOrderList:
                    if not (itemID in obj.currentOrderList):
                        continue
                
                productObj = productsTablePrimary.objects.filter(modelNumber=itemID)
                productTotalCost = 0
                for objData in productObj:
                    totalItemQuantity += itemQuantity
                    productTotalCost = objData.price * itemQuantity
                    productsTotalCost += productTotalCost
                    tokenAmount += productTotalCost * (tokenPercentage / 100)
                    
        orderSummery["totalItems"] = totalItemQuantity
        orderSummery["itemsPrice"] = toCommaSeperatedCurrency(productsTotalCost)
        promoDiscount = productsTotalCost * (discountPercentage / 100)
        promoDiscount = round(promoDiscount)
        orderSummery["promoDiscount"] = toCommaSeperatedCurrency(promoDiscount)
        deliveryCharge = productsTotalCost * (deliveryChargePercentage / 100)
        deliveryCharge = round(deliveryCharge)
        if deliveryCharge > 40:
            deliveryCharge = 40
        orderSummery["deliveryCharge"] = toCommaSeperatedCurrency(deliveryCharge)

        orderTotal = (productsTotalCost - promoDiscount) + deliveryCharge
        orderSummery["orderTotal"] = toCommaSeperatedCurrency(orderTotal)

        if obj.selectedMode == "token":
            orderSummery["isToken"] = 1
            orderSummery["token"] = toCommaSeperatedCurrency(int(tokenAmount))
            restAmount = orderTotal - int(tokenAmount)
            orderSummery["restAmount"] = toCommaSeperatedCurrency(restAmount)
            obj.tokenAmount = int(tokenAmount)
            obj.restAmount = int(restAmount)
            obj.orderTotal = int(orderTotal)
        else:
            orderSummery["isToken"] = 0
            obj.tokenAmount = 0
            obj.restAmount  = int(orderTotal)
            obj.orderTotal  = int(orderTotal)    

        dataDict['orderSummery'] = orderSummery

        deleveryAddress = []
        userAddrObj = userAddressBook.objects.filter(userId=request.user.id).filter(id=int(obj.deleveryAddressId))
        for addrData in userAddrObj: #todo remove camel case when already implimentt toCamelCase address save
            fullName = addrData.firstName + " " + addrData.lastName
            deleveryAddress.append(fullName)
            if addrData.locationType:
                deleveryAddress.append(addrData.locationType)
            deleveryAddress.append(addrData.address)
            deleveryAddress.append(addrData.landmark)
            deleveryAddress.append(addrData.townOrCity)
            stateAndZipCode = addrData.state + ", " + addrData.postcodeOrZIP
            deleveryAddress.append(stateAndZipCode)
            deleveryAddress.append(addrData.country)
            phoneNumber = "Phone: " + addrData.phoneNo
            deleveryAddress.append(phoneNumber)
        dataDict["deleveryAddress"] = deleveryAddress

        paymentMethod = {}
        if obj.paymentModeId == "upi":
            paymentMethod['method'] = "UPI"
            paymentMethod['id'] = obj.cvvOrUpi
        else:
            userPayObj = userPaymentTable.objects.filter(userId=request.user.id).filter(id=int(obj.accId))
            for objData in userPayObj:
                paymentMethod['method'] = objData.bankName + " " + objData.cardType
                paymentMethod['id'] = "ending in **" + objData.cardNumber[-4:]

        dataDict["paymentMethod"] = paymentMethod
        dataDict['isPromoCodeWrong'] = isPromoCodeWrong

        obj.save()

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}

    context = {
        'headerDict'    :   headerDict,
        'dataDict' : dataDict
    }
    return render(request, "product/purchase/reviewOrderBeforePayment.html", context)


def processTopay_View(request):

    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)
    dataDict = {}
    tempObj = temporaryOrderStoreTable.objects.filter(userId=request.user.id)
    for obj in tempObj:
        dataDict["tokenAmount"] = toCommaSeperatedCurrency(obj.tokenAmount)
        dataDict["restAmount"]  = toCommaSeperatedCurrency(obj.restAmount)
        dataDict["orderTotal"]  = toCommaSeperatedCurrency(obj.orderTotal)

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
        'headerDict'    :   headerDict,
        'dataDict' : dataDict
    }
    return render(request, "product/purchase/processTopay.html", context)

def placeOrder_View(request):
    paymentObj = paymentTable.objects.values_list()
    dataDict = {}
    for obj in paymentObj:
        if dataDict.__contains__(obj[1]):
            dataDict[obj[1]].append(obj) 
        else:
            dataDict[obj[1]] = [obj]
    print("paymentObj::", dataDict)
    
    context = {
        
        "paymentObj" : dataDict
    }
    return render(request, "product/purchase/placeOrder.html", context)
    

def login_View(request):
    print("login_View")

    if request.user.id != None:
        userObjects = usertable.objects.filter(userId=request.user.id)
        for userObject in userObjects:
            user = auth.authenticate(userObject.username, password=userObject.password)
            auth.logout(request)

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        redirectUrl = ""
        if request.session.__contains__("redirectedPageUrl"):
            redirectUrl = getSession(request, 'redirectedPageUrl')

        if user is not None:
            auth.login(request, user)   #redirectUrl used because after that request doesnot have session key
            setSession(request, 'redirectedPageUrl', redirectUrl)

            if redirectUrl == "":
                return redirect('/')
            else:
                return redirect(redirectUrl)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Invalid Credentials")
            return redirect("/login")
    else:
        print("login_view GET Method called")
        headerDict = {"userID" : ""}
        return render(request, 'loginRegister/login.html', {"headerDict" : headerDict})

def register_View(request, typeOfUser="customer"):
    print("register_View")

    if request.method == 'POST':
        firstName   = toCamelCase(request.POST['firstName'])
        lastName    = toCamelCase(request.POST['lastName'])
        gender      = toCamelCase(request.POST['gender'])
        password    = request.POST['password']
        mobileNumber    = request.POST['mobileNumber']
        whatsappNumber  = request.POST['whatsappNumber']
        emailAddress    = (request.POST['emailAddress']).lower()

        username = firstName.lower() + lastName.lower()
        testUserName = username
        while(True):
            counter = 0
            if User.objects.filter(username=testUserName).exists():
                counter += 1
                testUserName =  username + str(counter)
            else:
                username = testUserName
                break
        print("username created::", username)

        user = User.objects.create_user(username=username, password=password, email=emailAddress)
        user.save()
        usertable_ = usertable( userId=user.id, typeOfUser=typeOfUser, username=username, 
                                firstName=firstName, lastName=lastName, 
                                gender=gender, password=password, mobileNumber=mobileNumber, 
                                whatsappNumber=whatsappNumber, emailAddress=emailAddress)
        usertable_.save()
        
        for obj in webCredentialsTable.objects.filter(credentialType="sentEmail"):
            taskDataDict = { "operation" : "credentials" }
            taskDataDict["useremail"]  = emailAddress
            taskDataDict["username"]        = username
            taskDataDict["userPassword"]    = password
            
            threadPool =  myThreadPool()
            threadPool.addTaskToThreadPool("sentEmail", taskDataDict)
            
            messages.set_level(request, messages.INFO)
            msg = "your username::" + username + " | password::" + password
            messages.info(request, msg)
            #messages.info(request, "username and password sent through email")
            '''
            del request.session["firstName"]
            del request.session["lastName"]
            del request.session["mobileNumber"]
            del request.session["whatsappNumber"]
            del request.session["emailAddress"]
            '''
            return redirect('/login')
    
    else:
        headerDict = {"userID" : ""}
        context = {
            "headerDict" : headerDict,
        }
        return render(request, 'loginRegister/register.html', context)

