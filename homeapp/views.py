import json, datetime
from pickle import TRUE
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
                    paymentTable, tickerTable


from django.contrib.auth.models import User, auth

from .commom import  setSession, getSession

from .helper import alterProductManagePOST, handleSearchBox

def manager_default_View(request):
    return manager_View(request, "home")

def manager_View(request, touds):
    print("Manager::", touds)
    secondTouds = ""
    productId = ""


    print("-----------Old----Touds---------", touds)    
    print("-----------Old----secondTouds---------", secondTouds)
    if touds != "alterProduct": #todo remove this written for only testing purpose
        touds = "alterProduct"  
        secondTouds = "home"
    

    print("manager_View 1")
    if touds == "alterProduct":
        print("manager_View 2")
        secondTouds = "home"
    print("manager_View 3")
    if request.method == 'POST':
        print("manager_View POST 4")
        if request.POST.__contains__("formAddProductAction"):
            print("manager_View POST 5")
            request, secondTouds, productId = alterProductManagePOST(request)
            print("manager_View POST 6")
        else:
            print("manager_View POST 7")
            print("other posibilities")
    print("manager_View 8")




    categoryList = []
    if secondTouds == "primaryDetails":
        for obj in tickerTable.objects.values_list():
            categoryList = [ item.split("|")[0] for item in obj[2].replace("[", "").replace("]", "").replace("'", "").split(", ")]

    #secondTouds = "primaryDetails"
    #secondTouds = "moreDetails"
    #secondTouds = "hoverImages"
    #secondTouds = "descriptionAndSpacificationManage"

    tickerList = []
    if secondTouds == "moreDetails":
        for obj in tickerTable.objects.values_list():
            tickerList = [ item.split("|")[0] for item in obj[1].replace("[", "").replace("]", "").replace("'", "").split(", ")]
            
        print("tickerList::", tickerList)



    print("---------------Touds---------", touds)    
    print("---------------secondTouds---------", secondTouds)
    
    context = {
        "touds" : touds,
        "secondTouds" : secondTouds, 
        "productId" : productId,
        "categoryList" : categoryList,
        "tickerList" : tickerList
    }
    return render(request, "manager/index.html", context)


def Home_view(request):
    print("Home_view")

    if request.method == 'POST':
        print("Home_view POST::", request.POST)

        if(request.POST.__contains__("search")):
            url, matchNotFound, relaventSearch = handleSearchBox(request)
            setSession(request, 'matchNotFound', matchNotFound)
            setSession(request, 'relaventSearch', relaventSearch)
            #request.session['matchNotFound'] = matchNotFound
            #request.session['relaventSearch'] = relaventSearch
            if url != "":
                return redirect(url)

        elif (request.user.id == None) or (not usertable.objects.filter(userId=request.user.id).exists()):
            setSession(request, 'lastPageUrl', request.get_full_path())
            #request.session['lastPageUrl'] = request.get_full_path()
            print("Home_view 0 POST request.session['lastPageUrl']::",getSession(request, 'lastPageUrl'))
            return redirect('/login')

    productHomeCategoryListObj = homeProductListImagesTable.objects.filter(isActive=True)
    productHomeSliderObj       = homeSliderImageTable.objects.filter(isActive=True)

    print("productHomeCategoryListObj::", productHomeCategoryListObj)
    print("productHomeSliderObj::", productHomeSliderObj)

    userID = ""
    if (request.user.id != None) and usertable.objects.filter(userId=request.user.id).exists():
        userID = request.user.id

    print("userID::", userID)
    context = {
        'userID'    :   userID,
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
            url, matchNotFound, relaventSearch = handleSearchBox(request)
            setSession(request, 'matchNotFound', matchNotFound)
            setSession(request, 'relaventSearch', relaventSearch)
            #request.session['matchNotFound'] = matchNotFound
            #request.session['relaventSearch'] = relaventSearch
            if url != "":
                return redirect(url)
        elif request.POST.__contains__("signIn"):
            setSession(request, 'lastPageUrl', request.get_full_path())
            #request.session['lastPageUrl'] = request.get_full_path()
            print("ProductList_view 0 POST request.session['lastPageUrl']::",getSession(request, 'lastPageUrl'))
            return redirect('/login')

    categoryObj     =   productsTablePrimary.objects.filter(category=categoryName)
    brandNameObj    =   categoryObj.values_list('brandName', flat=True).distinct()

    dataDict = {}
    for obj in brandNameObj:
        dataDict[obj] = categoryObj.filter(brandName=obj).count()

    print("ProductList_view dataDict::",dataDict)

    userID = ""
    if (request.user.id != None) and usertable.objects.filter(userId=request.user.id).exists():
        userID = request.user.id

    context = {
        'userID'        : userID,
        'dataDict'      : dataDict,
        'brandnameObj'  : brandNameObj,
        'brandnameObjCount' :   brandNameObj.count(),
        'categoryName'  : categoryName
    }
    return render(request, "product/searchItems.html", context)



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


    print("ProductSearchList_view START")
    productproductTitleListObj = productsTablePrimary.objects.filter(title__contains=productTitle)
    filterDict = {"PRICE_BL_2000" : 0, "PRICE_BTW_2000_3000" : 0, "PRICE_BTW_3000_4000" : 0, "PRICE_BTW_4000_5000" : 0, "PRICE_ABW_5000" : 0}
    SORTBY = 'Popularity'
    matchNotFound = ""
    relaventSearch = ""

    if request.session.__contains__("matchNotFound"):
        matchNotFound = request.session['matchNotFound']
    if request.session.__contains__("relaventSearch"):
        relaventSearch = request.session['relaventSearch']

    print("ProductSearchList_view matchNotFound, relaventSearch::",matchNotFound, relaventSearch)

    url = ""
    if request.method == 'POST':
        print("ProductSearchList_view POST::", request.POST)
        if(request.POST.__contains__("search")):
            url, matchNotFound1, relaventSearch1 = handleSearchBox(request)
            matchNotFound = matchNotFound1
            relaventSearch = relaventSearch1
        elif(request.POST.__contains__("FILTER:PRICE")):
            print("ProductSearchList_view FILTER:PRICE::",request.POST["FILTER:PRICE"])
            productproductTitleListObj = priceFilterCalculateObj(request.POST["filterDict"], productproductTitleListObj)
            print("ProductSearchList_view productproductTitleListObj::",productproductTitleListObj)

        elif(request.POST.__contains__("dropdownSortButton")):
            print("ProductSearchList_view dropdownSortButton::",request.POST["dropdownSortButton"])
            SORTBY = request.POST["dropdownSortButton"]
            print("ProductSearchList_view INITIAL productproductTitleListObj::",productproductTitleListObj)
            productproductTitleListObj = priceFilterCalculateObj(request.POST["dropdownSortButtonfilterDict"], productproductTitleListObj)

            matchNotFound = request.POST["dropdownSortButtonmatchNotFound"]
            relaventSearch = request.POST["dropdownSortButtonrelaventSearch"]

            print("productproductTitleListObj::",productproductTitleListObj)
            #todo handle other sort methods Newsest, Popularity --> currntly taken High to Low
            if request.POST["dropdownSortButton"] == "LTH":
                productproductTitleListObj = productproductTitleListObj.order_by('price')
            else:
                productproductTitleListObj = productproductTitleListObj.order_by('-price')

    if url != "":
        vec = url.split("/")
        productTitle = vec[3]

    print("ProductSearchList_view productTitle::",productTitle)

    userID = ""
    if (request.user.id != None) and usertable.objects.filter(userId=request.user.id).exists():
        userID = request.user.id


    print("ProductSearchList_view 3 matchNotFound, relaventSearch::", matchNotFound, relaventSearch)

    context = {
        'userID'            :   userID,
        'matchNotFound'     :   matchNotFound,
        'relaventSearch'    :   relaventSearch,
        'filterDict'        :   filterDict,
        'SORTBY'        :   SORTBY,
        'searchTitle'   :   productTitle,
        'productBrandnameListObj'        : productproductTitleListObj,
        'productBrandnameListObjCount'   : productproductTitleListObj.count(),
        'categoryName'                   : "",
        'brandName'                      : ""
    }
    return render(request, "product/searchItemsOnClick.html", context)


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
    
    productBrandnameListObj = productsTablePrimary.objects.filter(category=categoryName).filter(brandName=brandName)
    print("----------------", productBrandnameListObj.values())
    filterDict = {"PRICE_BL_2000" : 0, "PRICE_BTW_2000_3000" : 0, "PRICE_BTW_3000_4000" : 0, "PRICE_BTW_4000_5000" : 0, "PRICE_ABW_5000" : 0}
    SORTBY = 'Popularity'
    matchNotFound = ''
    relaventSearch = ''
    if request.method == 'POST':
        print("ProductListOnClick_view POST")

        if (request.user.id == None) or (not usertable.objects.filter(userId=request.user.id).exists()):
            setSession(request, 'lastPageUrl', request.get_full_path())
            #request.session['lastPageUrl'] = request.get_full_path()
            print("ProductListOnClick_view 0 POST request.session['lastPageUrl']::",getSession(request,'lastPageUrl'))
            return redirect('/login')
        print("request.user.id::",request.user.id)
        url = ""
        updateaddToCartID = ""

        if request.POST.__contains__("ADDTOCART"):
            print("ProductListOnClick_view request.POST['ADDTOCART']::", request.POST['ADDTOCART'])
            updateaddToCartID = request.POST['ADDTOCART']
            url = "/viewcart"
        elif request.POST.__contains__("BUYNOW"):
            print("ProductListOnClick_view request.POST['BUYNOW']::", request.POST['BUYNOW'])
            updateaddToCartID = request.POST['BUYNOW']
            url = "/product/purchase"
            setSession(request, 'currentOrderList', [updateaddToCartID])
            #request.session["currentOrderList"] = [updateaddToCartID]
        elif(request.POST.__contains__("search")):
            print("ProductListOnClick_view handleSearchBox")
            url, matchNotFound, relaventSearch = handleSearchBox(request)
            setSession(request, 'matchNotFound', matchNotFound)
            setSession(request, 'relaventSearch', relaventSearch)
            #request.session['matchNotFound'] = matchNotFound
            #request.session['relaventSearch'] = relaventSearch
            if url != "":
                return redirect(url)
        elif(request.POST.__contains__("FILTER:PRICE")):
            print("ProductListOnClick_view FILTER:PRICE::",request.POST["FILTER:PRICE"])
            productBrandnameListObj = priceFilterCalculateObj(request.POST["filterDict"], productBrandnameListObj)
            print("ProductListOnClick_view productBrandnameListObj::",productBrandnameListObj)

        elif(request.POST.__contains__("dropdownSortButton")):
            print("ProductListOnClick_view dropdownSortButton::",request.POST["dropdownSortButton"])
            SORTBY = request.POST["dropdownSortButton"]
            productBrandnameListObj = priceFilterCalculateObj(request.POST["dropdownSortButtonfilterDict"], productBrandnameListObj)

            matchNotFound = request.POST["dropdownSortButtonmatchNotFound"]
            relaventSearch = request.POST["dropdownSortButtonrelaventSearch"]

            print("productBrandnameListObj::",productBrandnameListObj)
            #todo handle other sort methods Newsest, Popularity --> currntly taken High to Low
            if request.POST["dropdownSortButton"] == "LTH":
                productBrandnameListObj = productBrandnameListObj.order_by('price')
            else:
                productBrandnameListObj = productBrandnameListObj.order_by('-price')

        else:
            print("ProductListOnClick_view some other case")

        userObject = usertable.objects.filter(userId=request.user.id)[0]
        print("ProductListOnClick_view POST userObject::", userObject)

        addToCartItemsDict = {}
        if updateaddToCartID != "":
            if userObject.addToCartItemsDict != "":
                print("ProductListOnClick_view userObject.addToCartItemsDict::",userObject.addToCartItemsDict)
                #addToCartItemsDict = dict( map(int, item.split(":")) for item in userObject.addToCartItemsDict.strip('}{').split(","))
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

    print("ProductListOnClick_view 2")

    userID = ""
    if (request.user.id != None) and usertable.objects.filter(userId=request.user.id).exists():
        userID = request.user.id


    print("ProductListOnClick_view 3 productBrandnameListObj::",productBrandnameListObj)

    context = {
        'userID'            :   userID,
        'matchNotFound'     :   "",
        'relaventSearch'    :   "",
        'productBrandnameListObj'        : productBrandnameListObj,
        'productBrandnameListObjCount'   : productBrandnameListObj.count(),
        'categoryName'                   : categoryName,
        'brandName'                      : brandName,
        'filterDict'        :   filterDict,
        'SORTBY'            :   SORTBY,
        'matchNotFound'     :   matchNotFound,
        'relaventSearch'    :   relaventSearch
    }
    return render(request, "product/searchItemsOnClick.html", context)


def Product_view(request, modelNumber):

    if modelNumber == "purchase":
        return productPurchase_View(request)

    print("Product_view::", request, " | ", modelNumber)

    if request.method == 'POST':
        print("Product_view POST")

        if(request.POST.__contains__("search")):
            url, matchNotFound, relaventSearch = handleSearchBox(request)
            setSession(request, 'matchNotFound', matchNotFound)
            setSession(request, 'relaventSearch', relaventSearch)
            #request.session['matchNotFound'] = matchNotFound
            #request.session['relaventSearch'] = relaventSearch
            if url != "":
                return redirect(url)
        elif (request.user.id == None) or (not usertable.objects.filter(userId=request.user.id).exists()):
            setSession(request, 'lastPageUrl', request.get_full_path())
            #request.session['lastPageUrl'] = request.get_full_path()
            print("Product_view 0 POST request.session['lastPageUrl']::",getSession(request, 'lastPageUrl'))
            return redirect('/login')

        url = ""
        updateaddToCartID = ""
        #updateaddToCartQuantity = ""

        print("Product_view 1 POST request.POST::",request.POST)
        if(request.POST.__contains__("ADDTOCART")):
            updateaddToCartID = request.POST['ADDTOCART']
            url = "/viewcart"
            #updateaddToCartQuantity = int(request.POST['QUANTITY'])
        else:
            print("Product_view request.POST['BUYNOW']::", request.POST['BUYNOW'])
            #id_title = (request.POST['BUYNOW']).split("/")
            #print("Product_view id_title::", id_title)
            #updateaddToCartID = id_title[0]
            updateaddToCartID = request.POST['BUYNOW']
            #updateaddToCartQuantity = int(id_title[1])
            url = "/product/purchase"
            setSession(request, 'currentOrderList', [updateaddToCartID])
            #request.session["currentOrderList"] = [updateaddToCartID]

        userObject = usertable.objects.filter(userId=request.user.id)[0]
        print("Product_view POST userObject::", userObject)

        addToCartItemsDict = {}
        if userObject.addToCartItemsDict != "":
            #addToCartItemsDict = dict( map(int,item.split(":")) for item in userObject.addToCartItemsDict.strip('}{').split(","))
            addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))

        print("Product_view POST addToCartItemsDict::", addToCartItemsDict)
        if addToCartItemsDict.__contains__(updateaddToCartID):
            addToCartItemsDict[updateaddToCartID] += 1#updateaddToCartQuantity
        else:
            addToCartItemsDict[updateaddToCartID] = 1#updateaddToCartQuantity

        userObject.addToCartItemsDict = str(addToCartItemsDict)
        userObject.save()

        print("Product_view url::", url)
        if url != "":
            return redirect(url)

    print("Product_view 1 modelNumber::",modelNumber, productsTableTernary.objects.filter(productId=modelNumber))
    

    print("Product_view 6::")
    dataData = {
        "HoverImageDict"  : productsTableTernary.objects.filter(productId=modelNumber)[0].getHoverImageDict(),
        "Highlight" : {},
        "Spacification" : {}
    }
    #print("Product_view 7::", productsTableSecodary.objects.filter(productId=modelNumber).values())
    #ignoreItems = ['id', 'productId']
    if productsTableSecodary.objects.filter(productId=modelNumber).exists():
        for key, value in productsTableSecodary.objects.filter(productId=modelNumber).values()[0].items():
            #if key not in ignoreItems and value != 'None' and value:
            if key != 'id' and key != 'productId' and value:
                value = value.split("|")
                dataData["Highlight"][value[0]] = value[1]  #todo
    

    print("Product_view 8::")
    userID = ""
    if (request.user.id != None) and usertable.objects.filter(userId=request.user.id).exists():
        userID = request.user.id

    context = {
        'userID'       :   userID,
        'instance'     :   productsTablePrimary.objects.filter(modelNumber=modelNumber)[0],
        'dataData'     :   dataData
    }
    return render(request, "product/detail.html", context)

def account_profileInformation_View(request):
    return account_View(request, "profileinformation")

def account_View(request, touds):

    if touds == "orders":
        return orders_View(request)

    dataShow = ""
    dataDictionary = {}
    userObject = usertable.objects.filter(userId=request.user.id)
    if len(userObject) == 0:
        context = {"url" : request.get_full_path()}
        return render(request, "404.html", context)
    else:
        userObject = userObject[0]

    print("account_View 0 userObject::", userObject)

    if request.method == "POST":
        print("I AM IN POST");
        if request.POST.__contains__("menuSwitch"):
            if request.POST["menuSwitch"] == "profileinformation":
                return redirect("/account")
            elif request.POST["menuSwitch"] == "manageaddresses":
                return redirect("/account/addresses")
            else:
                url = "/account/" + request.POST["menuSwitch"]
                return redirect(url)
        else:
            pass

    print("account_View touds::", touds)
    if touds =="profileinformation":
        dataDictionary = {"userId" : userObject.userId, "username" : userObject.username, 
                          "firstName" : userObject.firstName, "lastName" : userObject.lastName,
                          "emailaddress" : userObject.emailaddress,
                          "mobilenumber" : userObject.mobilenumber,"whatsappnumber" : userObject.whatsappnumber }
        dataShow = touds
    elif touds =="addresses":
        dataDictionary = {"username" : userObject.username }
        dataShow ="manageaddresses"
    elif touds =="changepassword":
        dataDictionary = {"username" : userObject.username }
        dataShow = touds
    elif touds =="logout":
        user = auth.authenticate(userObject.username, password=userObject.password)
        auth.logout(request)
        return redirect("/")
    else:
        dataDictionary = {"username" : userObject.username }
        dataShow = touds

    print("account_View 2 dataDictionary::", dataDictionary)
    context = {

       "dataShow" : dataShow,
       "dataDictionary"      : dataDictionary
    }
    return render(request,"user/account/index.html", context)

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
            #print("user_addToCart_View perform order", request.POST["PROCEEDTOBUYFORM"])
            addToCartItemsDict = dict( [item.split(":")[0].strip().strip("'"),int(item.split(":")[1].strip())]  for item in userObject.addToCartItemsDict.strip('}{').split(","))
            addToCartKeys = list(addToCartItemsDict.keys())
            #print("user_addToCart_View addToCartKeys::",addToCartKeys, request.POST["PROCEEDTOBUYFORM"])
            notPurchasedItemList = []
            print('request.POST["PROCEEDTOBUYFORM"]::', request.POST["PROCEEDTOBUYFORM"])
            if request.POST["PROCEEDTOBUYFORM"] !="[]":
                notPurchasedItemList = request.POST["PROCEEDTOBUYFORM"].strip("[]").split(",")
            outputList = list(set(addToCartKeys) - set(notPurchasedItemList)) + list(set(notPurchasedItemList) - set(addToCartKeys))
            setSession(request, 'currentOrderList', outputList)
            #request.session["currentOrderList"] = outputList
            print("user_addToCart_View currentOrderList::",getSession(request, "currentOrderList"))
            return redirect("/product/purchase")
        elif request.POST.__contains__("CHANGEDQUANTITY"):
            flgCHANGEDQUANTITY = True

        elif(request.POST.__contains__("search")):
            print("ProductListOnClick_view handleSearchBox")
            url, matchNotFound, relaventSearch = handleSearchBox(request)
            setSession(request, 'matchNotFound', matchNotFound)
            setSession(request, 'relaventSearch', relaventSearch)
            #request.session['matchNotFound'] = matchNotFound
            #request.session['relaventSearch'] = relaventSearch
            if url != "":
                return redirect(url)

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

def orders_View(request):
    '''
    userObject = usertable.objects.filter(userId=request.user.id)
    if len(userObject) == 0:
        context = {"url" : request.get_full_path()}
        return render(request, "404.html", context)
    else:
        userObject = userObject[0]

    print("orders_View 0 userObject::", userObject)
    '''

    if request.method == "POST":
        print("orders_View 0 request.POST", request.POST)
        if(request.POST.__contains__("search")):
            print("orders_View handleSearchBox")
            url, matchNotFound, relaventSearch = handleSearchBox(request)
            setSession(request, 'matchNotFound', matchNotFound)
            setSession(request, 'relaventSearch', relaventSearch)
            #request.session['matchNotFound'] = matchNotFound
            #request.session['relaventSearch'] = relaventSearch
            if url != "":
                return redirect(url)

    print("orders_View 1 orders")

    orderTrackingStatusDict = {
                                0: "Order not placed yet",
                                1: "Packing started [HP]",
                                2: "Packing started [FP]",
                                3: "Packed [HP]",
                                4: "Packed [FP]",
                                5: "Delivery started [HP]",
                                6: "Delivery started [FP]",
                                7: "Out for delivery:Picked by courier guy [HP]",
                                8: "Out for delivery:Picked by courier guy [FP]",
                                9: "Delivery guy on the way [HP]",
                                10: "Delivery guy on the way [FP]",
                                11: "Guy reached on delivery location [HP]",
                                12: "Guy reached on delivery location [FP]",
                                13: "Not deliverd to the customer not paid rest amount or cancel order [HP]",
                                14: "Deliverd to the customer with paid rest amount [HP]",
                                15: "Deliverd to the customer [FP]",
                                16: "canceled by admin:Due to wrong transaction ID [HP]",
                                17: "canceled by admin:due to wrong transaction ID [FP]",
                                18: "canceled by admin:product out of stock [HP]",
                                19: "canceled by admin:product out of stock [FP]",
                                20: "canceled by user, from::before delivery started Payment [HP]",
                                21: "canceled by user, from::before delivery started Payment [FP]",
                                22: "returned by user, from::door-step Payment [HP]",
                                23: "returned by user, from::door-step Payment [FP]",
                                24: "returned by user, from::after delivered::with delivery charge [FP][W-DC]",
                                25: "returned by user, from::after delivered::except delivery charge [FP][E-DC]"
                            }

    print("orders_View 1 request.user.id::",request.user.id)
    userordertable_list = userordertable.objects.filter(userId=request.user.id)
    print("orders_View 1 userordertable_list::",userordertable_list)
    productDictList = []
    for userordertable_ in userordertable_list:
        print("orders_View userordertable_.orderTrackingStatus::",userordertable_.orderTrackingStatus)
        statusVec = orderTrackingStatusDict[userordertable_.orderTrackingStatus].split(":")
        orderTrackingStatus = statusVec[0]
        reason = ""
        if len(statusVec) == 2:
            reason = statusVec[1]
        orderDeliveryAddressSplitdata   =   userordertable_.orderDeliveryAddress.split(",", 1)
        orderDeliveryAddressHeading     =   orderDeliveryAddressSplitdata[0]
        orderDeliveryAddressRestPart    =   orderDeliveryAddressSplitdata[1].split(",")
        print("orders_View userordertable_.orderPlacedDate::", str(userordertable_.orderPlacedDate).split("-"))

        payAtHome = 0
        warning = 0
        if userordertable_.paidAmount < userordertable_.finalPaidAmount:
            payAtHome = userordertable_.finalPaidAmount - userordertable_.paidAmount

        dataDict = { "orderPlacedDate" : userordertable_.orderPlacedDate, "finalPaidAmount" : userordertable_.finalPaidAmount,
                    "onOrderPaidAmount" : userordertable_.onOrderPaidAmount, "payAtHome" : payAtHome, "warning" : warning,
                    "orderDeliveryAddressHeading" : orderDeliveryAddressHeading, "orderDeliveryAddressRestPart" : orderDeliveryAddressRestPart,
                    "orderId" : userordertable_.orderId, "orderTrackingStatus" : orderTrackingStatus, "reason":reason,
                    "orderPaymentDate" : userordertable_.orderFirstPaymentDate, "orderedItemImage" : userordertable_.orderedItemImage,
                    "orderTitle" : userordertable_.orderTitle, "orderItemId" : userordertable_.orderItemId, "orderSellingQuantity" : userordertable_.orderSellingQuantity
        }
        productDictList.append(dataDict)

    dataDictionary = {}
    if len(productDictList) == 0:
        ordernotplaced = "Order Not Placed"
        dataDictionary = { "productDictList" : productDictList, "ordernotplaced" : ordernotplaced }
    else:
        dataDictionary = { "productDictList" : productDictList }

    print("orders_View 2 dataDictionary::", dataDictionary)
    context = {
        #"defaultUserDataShow" : defaultUserDataShow,
        "dataDictionary"      : dataDictionary
    }
    return render(request, "user/orders/index.html", context)


def productPurchase_View(request):
    print("productPurchase_View")
    userAddressBookList = []
    userAddressBookItemDelete = ""
    userAddressBookItemEditObj = ""

    userObjects = usertable.objects.filter(userId=request.user.id)
    print("productPurchase_View userObjects::", userObjects)

    if (request.user.id == None) or (len(userObjects) == 0):
        setSession(request, 'lastPageUrl', request.get_full_path())
        #request.session['lastPageUrl'] = request.get_full_path()
        print("productPurchase_View lastPageUrl::",request.get_full_path())
        return redirect('/login')
    elif request.method == 'POST':
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
            firstName       = request.POST['firstName']
            lastName        = request.POST['lastName']
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
                userAddressBook_ = userAddressBook(userId=request.user.id, firstName=firstName, lastName=lastName, companyName=companyName,
                                        countryOrRegion=countryOrRegion, streetAddress1=streetAddress1, streetAddress2=streetAddress2,
                                        townOrCity=townOrCity, stateOrCounty=stateOrCounty, postcodeOrZIP=postcodeOrZIP, phoneNo=phoneNo,
                                        emailAddress=emailAddress, orderNotes=orderNotes)
                userAddressBook_.save()

                for obj in userObjects:
                    #print("obj::", obj)
                    #print("obj.userAddressBooks", obj.userAddressBooks)
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
                #print("MODIFYADDRESS::", request.POST['MODIFYADDRESS'])
                userAddressBook_ = userAddressBook(id=int(request.POST['MODIFYADDRESS']), userId=request.user.id, firstName=firstName, lastName=lastName, companyName=companyName,
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
                dataDict["userFullName"]    = useraddressBookObj.firstName + " " + useraddressBookObj.lastName
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

    if (request.user.id == None) or (not usertable.objects.filter(userId=request.user.id).exists()):
        #print("productPaymentGateway_View 0 lastPageUrl::", request.get_full_path())
        setSession(request, 'lastPageUrl', request.get_full_path())
        #request.session['lastPageUrl'] = request.get_full_path()
        return redirect('/login')

    userObject = usertable.objects.filter(userId=request.user.id)[0]
    print("productPaymentGateway_View start userObject::", userObject)

    if userObject.addToCartItemsDict != "":
        print("userObject.addToCartItemsDict::", userObject.addToCartItemsDict)
        #addToCartItemsDict = dict( map(int,item.split(":")) for item in userObject.addToCartItemsDict.strip('}{').split(","))
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
            orderDeliveryAddress =  useraddressBookObj.firstName + " " + useraddressBookObj.lastName + ", " + useraddressBookObj.streetAddress1 + ", " + \
                        useraddressBookObj.streetAddress2 + ", " + useraddressBookObj.townOrCity + ", " + useraddressBookObj.stateOrCounty  + " " + \
                        useraddressBookObj.postcodeOrZIP + ", " + useraddressBookObj.countryOrRegion + ", " + "Contact No." + useraddressBookObj.phoneNo

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
        if request.session.__contains__("lastPageUrl"):
            redirectUrl = getSession(request, 'lastPageUrl')

        if user is not None:
            auth.login(request, user)   #redirectUrl used because after that request doesnot have session key
            setSession(request, 'lastPageUrl', redirectUrl)
            #request.session['lastPageUrl'] = redirectUrl

            if redirectUrl == "":
                return redirect('/')
            else:
                return redirect(redirectUrl)
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("/login")
    else:
        print("login_view GET Method called")
        return render(request, 'loginRegister/login.html')

def register_View(request):
    print("register_View")

    dataDict = {
        "firstName" : "", "lastName" : "", "username" : "", "password1" : "", "password2" : "", 
        "mobilenumber" : "", "whatsappnumber" : "", "emailaddress" : ""
    }
    
    if "firstName" in request.session:
        dataDict["firstName"]       = getSession(request, "firstName")
        dataDict["lastName"]        = getSession(request, "lastName")
        dataDict["password1"]       = getSession(request, "password1")
        dataDict["password2"]       = getSession(request, "password2")
        dataDict["mobilenumber"]    = getSession(request, "mobilenumber")
        dataDict["whatsappnumber"]  = getSession(request, "whatsappnumber")
        dataDict["emailaddress"]    = getSession(request, "emailaddress")
        
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = (request.POST['firstName'].lower()) + (request.POST['lastName'].lower())
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mobilenumber = request.POST['mobilenumber']
        whatsappnumber = request.POST['whatsappnumber']
        emailaddress = request.POST['emailaddress']
        #userImage = request.POST['userImage']

        setSession(request, 'firstName', firstName)
        setSession(request, 'lastName', lastName)
        setSession(request, 'password1', password1)
        setSession(request, 'password2', password2)
        setSession(request, 'mobilenumber', mobilenumber)
        setSession(request, 'whatsappnumber', whatsappnumber)
        setSession(request, 'emailaddress', emailaddress)
        
        #request.session["firstName"] = firstName
        #request.session["lastName"] = lastName
        #request.session["password1"] = password1
        #request.session["password2"] = password2
        #request.session["mobilenumber"] = mobilenumber
        #request.session["whatsappnumber"] = whatsappnumber
        #request.session["emailaddress"] = emailaddress

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User Already Taken")
                return redirect('/register')

            elif User.objects.filter(email=emailaddress).exists():
                messages.info(request, "Email Already Taken")
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=emailaddress)
                usertable_ = usertable(userId=user.id, username=username, firstName=firstName, 
                                        lastName=lastName, password=password1,
                                        mobilenumber=mobilenumber, whatsappnumber=whatsappnumber,
                #                        userImage=userImage, emailaddress=emailaddress)
                                        emailaddress=emailaddress)
                usertable_.save()
                user.save()

                messages.info(request, "User Created")
        else:
            messages.info(request, "Password Mismatch")
            #return redirect('/register')
            context = {
                "dataDict" : dataDict
            }
            return render(request, 'loginRegister/register.html', context)

        del request.session["firstName"]
        del request.session["lastName"]
        del request.session["password1"]
        del request.session["password2"]
        del request.session["mobilenumber"]
        del request.session["whatsappnumber"]
        del request.session["emailaddress"]

        return redirect('/login')
    else:
        context = {
            "dataDict" : dataDict
        }
        return render(request, 'loginRegister/register.html', context)

