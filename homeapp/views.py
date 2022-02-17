import json, datetime

from pickle import TRUE
from threading import *
from posixpath import split
#import re
from urllib import response
from urllib.request import Request
from django.contrib import messages
from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
from .models import usertable, userAddressBook, userordertable, userOrderGrouptable, \
                    homeSliderImageTable, homeProductListImagesTable,\
                    productsTablePrimary, productsTableSecodary, productsTableTernary, \
                    paymentTable, webCredentialsTable

from django.contrib.auth.models import User, auth

from .commom import  setSession, getSession, myThreadPool

from .helper import searchContentInSearchBar, checkUserLogged, getUserId

def Home_view(request):
    print("Home_view")

    if request.method == 'POST':
        print("Home_view POST::", request.POST)

        if(request.POST.__contains__("search")):
            return searchContentInSearchBar(request)
        else:
            checkUserLogged(request, request.get_full_path())

    productHomeCategoryListObj = homeProductListImagesTable.objects.filter(isActive=True)
    productHomeSliderObj       = homeSliderImageTable.objects.filter(isActive=True)

    print("productHomeCategoryListObj::", productHomeCategoryListObj)
    print("productHomeSliderObj::", productHomeSliderObj)

    context = {
        'userID'    :   getUserId(request),
        'productHomeCategoryListObj'        : productHomeCategoryListObj,
        'productHomeCategoryListObjCount'   : productHomeCategoryListObj.count(),
        'productHomeSliderObj'              : productHomeSliderObj,
        'productHomeSliderObjCountList'     : list(range(0, productHomeSliderObj.count())),
    }
    return render(request, "home/index.html", context)

def ProductList_view(request, categoryName):
    print("ProductList_view")

    if request.method == 'POST':
        print("ProductList_view request.POST::",request.POST)
        if request.POST.__contains__("search"):
            return searchContentInSearchBar(request)
        else:
            checkUserLogged(request, request.get_full_path())
        
    categoryObj     =   productsTablePrimary.objects.filter(category=categoryName).filter(isActive=True)
    brandNameObj    =   categoryObj.values_list('brandName', flat=True).distinct()

    dataDict = {}
    for obj in brandNameObj:
        dataDict[obj] = categoryObj.filter(brandName=obj).count()

    print("ProductList_view dataDict::",dataDict)

    context = {
        'userID'        : getUserId(request),
        'dataDict'      : dataDict,
        'brandnameObj'  : brandNameObj,
        'brandnameObjCount' :   brandNameObj.count(),
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
            print("ProductSearchList_view FILTER:PRICE::",request.POST["FILTER:PRICE"])
            productproductTitleListObj = priceFilterCalculateObj(request.POST["filterDict"], productproductTitleListObj)
            print("ProductSearchList_view productproductTitleListObj::",productproductTitleListObj)

        elif(request.POST.__contains__("dropdownSortButton")):
            print("ProductSearchList_view dropdownSortButton::",request.POST["dropdownSortButton"])
            SORTBY = request.POST["dropdownSortButton"]
            print("ProductSearchList_view INITIAL productproductTitleListObj::",productproductTitleListObj)
            productproductTitleListObj = priceFilterCalculateObj(request.POST["dropdownSortButtonfilterDict"], productproductTitleListObj)
            print("productproductTitleListObj::",productproductTitleListObj)
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

    context = {
        'userID'            :   getUserId(request),
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
            checkUserLogged(request, request.get_full_path())
            
            if request.POST.__contains__("ADDTOCART"):
                print("ProductListOnClick_view request.POST['ADDTOCART']::", request.POST['ADDTOCART'])
                updateaddToCartID = request.POST['ADDTOCART']
                url = "/viewcart"
            elif request.POST.__contains__("BUYNOW"):
                print("ProductListOnClick_view request.POST['BUYNOW']::", request.POST['BUYNOW'])
                updateaddToCartID = request.POST['BUYNOW']
                url = "/product/purchase"
                setSession(request, 'currentOrderList', [updateaddToCartID])
             
            if url != "":
                return redirect(url)
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
                #todo pradeep
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

        if url != "":
            return redirect(url)

    else:
        #todo if any error came
        print("Method is GET Bada dikkat he re deva....")

    print("ProductListOnClick_view 3 productBrandnameListObj::",productBrandnameListObj)

    context = {
        'userID'            :   getUserId(request),
        'productBrandnameListObj'        : productBrandnameListObj,
        'productBrandnameListObjCount'   : productBrandnameListObj.count(),
        'categoryName'                   : categoryName,
        'brandName'                      : brandName,
        'filterDict'        :   filterDict,
        'searchTitle'   :   "",
        'SORTBY'            :   SORTBY,
        'searchContent'     :   brandName,
    }
    return render(request, "product/search/fromTitle.html", context)


def Product_view(request, modelNumber):

    if modelNumber == "purchase":
        return productPurchase_View(request)

    print("Product_view::", request, " | ", modelNumber)

    if request.method == 'POST':
        print("Product_view POST")

        if(request.POST.__contains__("search")):
            return searchContentInSearchBar(request)
        else:
            checkUserLogged(request, request.get_full_path())
        
        url = ""
        updateaddToCartID = ""
        
        print("Product_view 1 POST request.POST::",request.POST)
        if(request.POST.__contains__("ADDTOCART")):
            updateaddToCartID = request.POST['ADDTOCART']
            url = "/viewcart"
        else:
            print("Product_view request.POST['BUYNOW']::", request.POST['BUYNOW'])
            updateaddToCartID = request.POST['BUYNOW']
            url = "/product/purchase"
            setSession(request, 'currentOrderList', [updateaddToCartID])
           
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
        if url != "":
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
    context = {
        'userID'       :   getUserId(request),
        'instance'     :   productsTablePrimary.objects.filter(modelNumber=modelNumber)[0],
        'dataData'     :   dataData
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
            setSession(request, 'currentOrderList', outputList)
            print("user_addToCart_View currentOrderList::",getSession(request, "currentOrderList"))
            return redirect("/product/purchase")
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
            productObj = productsTablePrimary.objects.filter(modelNumber=itemID)
            if len(productObj) == 1:
                productDictList.append({ "itemID" : itemID, "title" : productObj[0].title, 
                                        "price" : productObj[0].price, "imageurl": productObj[0].mainImage.url, 
                                        "quantity" : itemQuantity, "storeQuantity" : productObj[0].quantity } )
                itemidList.append(itemID)
                totalQuantity += itemQuantity
                subtotal += (productObj[0].price * itemQuantity)
            else:
                #TODO << Item out of stock >>
                print("WE have issue at productPaymentGateway productObj...", len(productObj))

        dataDictionary = {"productDictList" : productDictList, "itemidList" : itemidList,"totalQuantity":totalQuantity,"subtotal" : subtotal}
    else:
        print("user_addToCart_View 1 add-to-cart ELSE")
        dataDictionary = {"productDictList" : [], "itemidList" : [],"totalQuantity": 0,"subtotal" : 0}

    print("user_addToCart_View 2 dataDictionary::", dataDictionary)
    
    if dataDictionary["productDictList"] == []:
        return redirect("/")

    context = {
       "dataDictionary"      : dataDictionary
    }
    return render(request,"user/addToCart/index.html", context)

def productPurchase_View(request):
    
    checkUserLogged(request, request.get_full_path())

    print("productPurchase_View")
    userAddressBookList = []
    userAddressBookItemDelete = ""
    userAddressBookItemEditObj = ""

    userObjects = usertable.objects.filter(userId=request.user.id)
    print("productPurchase_View userObjects::", userObjects)

    if request.method == 'POST':
        print("request POST::",request.POST)
        print("request POST userObjects::",userObjects)

        if "EDIT" in request.POST.keys() or "DELETE" in request.POST.keys():
            print("productPurchase_View Address EDIT or DELETE")
            if "EDIT" in request.POST.keys() and request.POST['EDIT'] != "":
                userAddressBookItemEditObj = userAddressBook.objects.filter(id=int(request.POST['EDIT']))[0]
            elif request.POST['DELETE'] != "":
                userAddressBookItemDelete = int(request.POST['DELETE'])
        else:
            print("productPurchase_View Address alter")
            firstname       = request.POST['firstname']
            lastname        = request.POST['lastname']
            companyName     = request.POST['companyName']
            countryOrRegion = request.POST['countryOrRegion']
            streetAddress1  = request.POST['streetAddress1']
            streetAddress2  = request.POST['streetAddress2']
            townOrCity      = request.POST['townOrCity']
            stateOrCounty   = request.POST['stateOrCounty']
            postcodeOrZIP   = request.POST['postcodeOrZIP']
            phoneNo         = request.POST['phoneNo']
            emailAddress    = request.POST['emailAddress']
            orderNotes      = request.POST['orderNotes']

            print("productPurchase_View 1")

            if "MODIFYADDRESS" not in request.POST.keys():
                print("productPurchase_View address:: Add new address")
                userAddressBook_ = userAddressBook(userId=request.user.id, firstname=firstname, lastname=lastname, companyName=companyName,
                                        countryOrRegion=countryOrRegion, streetAddress1=streetAddress1, streetAddress2=streetAddress2,
                                        townOrCity=townOrCity, stateOrCounty=stateOrCounty, postcodeOrZIP=postcodeOrZIP, phoneNo=phoneNo,
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
                print("productPurchase_View Address Modify")
                userAddressBook_ = userAddressBook(id=int(request.POST['MODIFYADDRESS']), userId=request.user.id, firstname=firstname, 
                                        lastname=lastname, companyName=companyName,
                                        countryOrRegion=countryOrRegion, streetAddress1=streetAddress1, streetAddress2=streetAddress2,
                                        townOrCity=townOrCity, stateOrCounty=stateOrCounty, postcodeOrZIP=postcodeOrZIP, phoneNo=phoneNo,
                                        emailAddress=emailAddress, orderNotes=orderNotes)
                userAddressBook_.save()

        print("productPurchase_View ListOfAddress_1::create userAddressBookList for list of address")
        for obj in userObjects:
            print("obj::",obj)
            print("obj.userAddressBooks::",obj.userAddressBooks)
            if (obj.userAddressBooks != "") and (obj.userAddressBooks != "[]"):
                if userAddressBookItemEditObj == "":
                    userAddressBookList = list(map(int, obj.userAddressBooks.strip('][').split(', ')))
                if userAddressBookItemDelete != "":
                    print("userAddressBookList, userAddressBookItemDelete::", userAddressBookList, userAddressBookItemDelete)
                    userAddressBookList.remove(userAddressBookItemDelete)
                    userAddressBookItemDelete = ""
                    obj.userAddressBooks = str(userAddressBookList)
                    obj.save()
        print("userAddressBookList::",userAddressBookList)
    else:
        #todo GET METHOD
        print("productPurchase_View GET METHOD :: show user all list of address on top of page")
        for obj in userObjects:
            print("ELSE obj.userAddressBooks::", obj.userAddressBooks)
            if (obj.userAddressBooks != "") and (obj.userAddressBooks != "[]"):
                userAddressBookList = list(map(int, obj.userAddressBooks.strip('][').split(', ')))

    userAddressBookDictList = []
    if userAddressBookList != []:
        print("productPurchase_View ListOfAddress_2::create userAddressBookList for list of address")
        for idData in userAddressBookList:
            useraddressBookObj = userAddressBook.objects.filter(id=idData)
            if len(useraddressBookObj) == 1:
                useraddressBookObj = useraddressBookObj[0]
                dataDict = {}
                dataDict["id"] = idData
                dataDict["userFullName"]    = useraddressBookObj.firstname + " " + useraddressBookObj.lastname
                dataDict["addr1"]   = useraddressBookObj.streetAddress1
                dataDict["addr2"]   = useraddressBookObj.streetAddress2
                dataDict["townCity"]= useraddressBookObj.townOrCity + ", " + useraddressBookObj.stateOrCounty  + " " + useraddressBookObj.postcodeOrZIP
                dataDict["countryOrRegion"]  = useraddressBookObj.countryOrRegion
                dataDict["phoneNo"]  = useraddressBookObj.phoneNo
                dataDict["orderNotes"]       = useraddressBookObj.orderNotes
                userAddressBookDictList.append(dataDict)
            else:
                print("WE have issue at productPurchase_View ListOfAddress_2...", len(useraddressBookObj))

    print("productPurchase_View END")

    context = {
        "userID"                        :   request.user.id,
        "userAddressBookDictList"       :   userAddressBookDictList,
        "userAddressBookDictListCount"  :   len(userAddressBookDictList),
        "userAddressBookItemEditObj"    :   userAddressBookItemEditObj
    }
    return render(request, "product/purchase/index.html", context)

def productPaymentGateway_View(request, addressId):
    print("productPaymentGateway_View...")

    checkUserLogged(request, request.get_full_path())

    userObject = usertable.objects.filter(userId=request.user.id)[0]
    print("productPaymentGateway_View start userObject::", userObject)

    if userObject.addToCartItemsDict != "":
        print("userObject.addToCartItemsDict::", userObject.addToCartItemsDict)
        addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))
    orderDeliveryAddress = ""

    if request.method == 'POST':
        if request.POST.__contains__("CHANGEDQUANTITY"): #click on update button after change quantity
            print("productPaymentGateway_View click on update button request.POST", request.POST)
            updateditemquantity = ""
            updateditemID = ""
            orderDeliveryAddress    = request.POST["DELIVERYADDRESS"]
            updateditemquantity     = int(request.POST["CHANGEDQUANTITY"])
            updateditemID           = request.POST["ITEMID"]

            if updateditemquantity != 0:
                addToCartItemsDict[updateditemID] = updateditemquantity
                print("productPaymentGateway_View 1 if updateditemquantity::", updateditemquantity)
            else:
                del addToCartItemsDict[updateditemID]
                print("productPaymentGateway_View 1 else updateditemquantity::", updateditemquantity)

            if addToCartItemsDict == {}:
                userObject.addToCartItemsDict = ""
            else:
                userObject.addToCartItemsDict = str(addToCartItemsDict)
            userObject.save()
        else: #when click on Place Order after payment contain ORDERFIRSTTRXNID
            print("productPaymentGateway_View Place order button click request.POST", request.POST)
            orderDeliveryAddress        = request.POST["DELIVERYADDRESS"]
            onOrderPaidAmount           = request.POST["onOrderPaidAmount"]
            orderFirstPaidTrxnID        = request.POST['ORDERFIRSTTRXNID']
            orderFirstPaymentID         = request.POST['PAYMENTID']

            userOrderGrouptable_ = userOrderGrouptable(userId=request.user.id, ordersList="")
            typeofpayment = False
            if request.POST['TYPEOFPAYMENT'] == "PARTIAL":
                typeofpayment = False
            else:
                typeofpayment = True

            addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))

            orderTableIdList = []
            for itemID, itemQuantity in addToCartItemsDict.items():
                if request.session.__contains__("currentOrderList"):
                    if not (itemID in getSession(request, "currentOrderList")):
                        continue
                productObjs = productsTablePrimary.objects.filter(modelNumber=itemID)
                for productObj in productObjs:
                    print("productPaymentGateway_View userordertable started for ::", itemID)
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
                    print("productPaymentGateway_View userordertable END for ::", itemID)
                    productObj.quantity -= itemQuantity
                    productObj.save()
                
            userOrderGrouptable_.ordersList = str(orderTableIdList)
            userOrderGrouptable_.save()

            print("productPaymentGateway_View userOrderGrouptable::", userOrderGrouptable_)

            for id in orderTableIdList:
                userordertable_ = userordertable.objects.filter(id=id)[0]
                userordertable_.orderId = str(request.user.id) + "-" + str(userOrderGrouptable_.id) + "-" + str(userordertable_.id)
                userordertable_.save()

            print("productPaymentGateway_View orderId updated in userordertable")

            if request.session.__contains__("currentOrderList"):
                for itemID in getSession(request, "currentOrderList"):
                    del addToCartItemsDict[itemID]
                del request.session["currentOrderList"]

            if addToCartItemsDict == {}:
                userObject.addToCartItemsDict = ""
            else:
                userObject.addToCartItemsDict = str(addToCartItemsDict)

            userObject.save()

            url = "/account/orders"

            print("productPaymentGateway_View 1 else url::", url)

            return redirect(url)

    if orderDeliveryAddress == "":
        useraddressBookObj = userAddressBook.objects.filter(id=addressId)
        if len(useraddressBookObj) == 1:
            useraddressBookObj = useraddressBookObj[0]
            orderDeliveryAddress =  useraddressBookObj.firstname + " " + useraddressBookObj.lastname + ", " + \
                        useraddressBookObj.streetAddress1 + ", " + useraddressBookObj.streetAddress2 + ", " + \
                        useraddressBookObj.townOrCity + ", " + useraddressBookObj.stateOrCounty  + " " + \
                        useraddressBookObj.postcodeOrZIP + ", " + useraddressBookObj.countryOrRegion + ", " + \
                        "Contact No." + useraddressBookObj.phoneNo

            print("orderDeliveryAddress: ", orderDeliveryAddress)
        else:
            print("WE have issue at productPaymentGateway useraddressBookObj...", len(useraddressBookObj))

    print("productPaymentGateway_View 4 addToCartItemsDict::", addToCartItemsDict)
    print("request.session['currentOrderList']::", getSession(request, "currentOrderList"))
    productDictList = []
    productsTotalCost = 0
    productsPartialCost = 0
    itemidList  =  []
    for itemID, itemQuantity in addToCartItemsDict.items():
        if request.session.__contains__("currentOrderList"):
            if not (itemID in getSession(request, "currentOrderList")):
                continue
        productObj = productsTablePrimary.objects.filter(modelNumber=itemID)
        if len(productObj) == 1:
            productDictList.append({ "itemID" : itemID, "title" : productObj[0].title, "price" : productObj[0].price, "quantity" : itemQuantity, "storeQuantity": productObj[0].quantity})
            productTotalCost = productObj[0].price * itemQuantity
            productsTotalCost += productTotalCost
            productsPartialCost += productTotalCost * (20/100)
            itemidList.append(itemID)
        else:
            #TODO << Item out of stock >>
            print("WE have issue at productPaymentGateway productObj...", len(productObj))

    paymentObj = paymentTable.objects.values_list()
    dataDict = {}
    for obj in paymentObj:
        if dataDict.__contains__(obj[1]):
            dataDict[obj[1]].append(obj) 
        else:
            dataDict[obj[1]] = [obj]
    print("paymentObj::", dataDict)

    print("itemidList::", itemidList)
    if(len(itemidList) == 0):
        return redirect("/")
        

    context = {
        "orderDeliveryAddress"      : orderDeliveryAddress,
        "productDictList"           : productDictList,
        "itemidList"                : itemidList,
        "productsTotalCost"         : productsTotalCost,
        "productsPartialCost"       : round(productsPartialCost),
        "paymentObj"                : dataDict
    }

    return render(request, "product/purchase/payment.html", context)

def login_View(request):
    print("login_View")

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
            messages.info(request, "Invalid Credentials")
            return redirect("/login")
    else:
        print("login_view GET Method called")
        return render(request, 'loginRegister/login.html', {"userID" : "",})

def register_View(request):
    print("register_View")

    dataDict = {
        "firstname" : "", "lastname" : "", "username" : "",  "mobilenumber" : "", "whatsappnumber" : "", "emailaddress" : ""
    }
    
    if "firstname" in request.session:
        dataDict["firstname"]       = getSession(request, "firstname")
        dataDict["lastname"]        = getSession(request, "lastname")
        dataDict["mobilenumber"]    = getSession(request, "mobilenumber")
        dataDict["whatsappnumber"]  = getSession(request, "whatsappnumber")
        dataDict["emailaddress"]    = getSession(request, "emailaddress")
        
    if request.method == 'POST':
        firstname = (request.POST['firstname']).lower()
        lastname = (request.POST['lastname']).lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mobilenumber = request.POST['mobilenumber']
        whatsappnumber = request.POST['whatsappnumber']
        emailaddress = (request.POST['emailaddress']).lower()

        setSession(request, 'firstname', firstname)
        setSession(request, 'lastname', lastname)
        setSession(request, 'mobilenumber', mobilenumber)
        setSession(request, 'whatsappnumber', whatsappnumber)
        setSession(request, 'emailaddress', emailaddress)
        context = {
            "userID" : "",
            "dataDict" : {"firstname" : firstname, "lastname" : lastname, "mobilenumber" : mobilenumber, 
                            "whatsappnumber" : whatsappnumber, "emailaddress" : emailaddress}
        }
        if password1 == password2:
            if len(password1) < 6 :
                messages.set_level(request, messages.ERROR)
                messages.error(request, "password should at least 6 digit")
                return render(request, 'loginRegister/register.html', context)
            elif User.objects.filter(email=emailaddress).exists():
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Email already taken")
                return render(request, 'loginRegister/register.html', context)
            
            else:
                username = firstname + lastname
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
                user = User.objects.create_user(username=username, password=password1, email=emailaddress)
                usertable_ = usertable(userId=user.id, username=username, firstname=firstname, 
                                        lastname=lastname, password=password1, mobilenumber=mobilenumber, 
                                        whatsappnumber=whatsappnumber, emailaddress=emailaddress)
                usertable_.save()
                user.save()

                for obj in webCredentialsTable.objects.filter(credentialType="sentEmail"):
                    websiteUrl  = obj.websiteUrl
                    senderEmail = obj.senderEmail
                    password    = obj.password
                    
                    subject = "User credentials"
                    messageContent = "<p><b><span style='color:green'> Congratulations!</b> now you are member of "+ websiteUrl +" </b></p>"
                    messageContent += "<p> Below are your login credentials </p>"
                    messageContent += "<p> Username : "+ username +" </p>"
                    messageContent += "<p> Password : "+ password +" </p>"
                    
                    taskDataDict = {}
                    taskDataDict["senderEmail"] = senderEmail
                    taskDataDict["emailaddress"] = emailaddress
                    taskDataDict["password"] = password
                    taskDataDict["subject"] = subject
                    taskDataDict["messageContent"] = messageContent

                    ''' #todo deamon thread
                    def initAddTaskToThreadPool():
                        addTaskToThreadPool("sentEmail", taskDataDict)
                    T = Thread(target = initAddTaskToThreadPool)
                    T.setDaemon(True)
                    T.start()
                    '''
                    threadPool =  myThreadPool()
                    threadPool.addTaskToThreadPool("sentEmail", taskDataDict)

                    messages.set_level(request, messages.INFO)
                    messages.info(request, "username and password sent through email")
                    del request.session["firstname"]
                    del request.session["lastname"]
                    del request.session["mobilenumber"]
                    del request.session["whatsappnumber"]
                    del request.session["emailaddress"]

                    return redirect('/login')
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "password mismatch")
            return render(request, 'loginRegister/register.html', context)
    else:
        context = {
            "userID" : "",
            "dataDict" : dataDict
        }
        return render(request, 'loginRegister/register.html', context)

