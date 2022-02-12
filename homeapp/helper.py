from django.contrib import messages
from .models import productsTablePrimary, productsTableSecodary, productsTableQuaterly, paymentTable, tickerTable

from .forms import ProductsTablePrimaryForm, ProductsTableTernaryForm, HomeSliderImageTableForm, \
        HomeProductListImagesTableForm


def updateTikerTableCategoryList(request):

    if len(tickerTable.objects.all()) == 0:
        tickerTable_ = tickerTable(tickerList="[]", categoryList=str([request.POST["category"]]), 
                        categoryTickerMapList="{}", categorySubCategoryMapList="{}")
        tickerTable_.save()
    else:
        for obj in tickerTable.objects.values_list():
            categoryList = []
            if obj[2] == "[]":
                categoryList.append(request.POST["category"])
            else:
                categoryList = [ item.split("|")[0] for item in obj[2].replace("[", "").replace("]", "").replace("'", "").split(", ")]
            
                if request.POST["category"] not in categoryList:
                    categoryList.append(request.POST["category"])

            for obj in tickerTable.objects.all():
                obj.categoryList = categoryList
                obj.save()


def updateTikerTableCategorySubCategoryMapList(request):

    for obj in tickerTable.objects.values_list():
        #print("obj::", obj)
        categorySubCategoryMapList = {}

        if obj[4] == "{}":
            categorySubCategoryMapList[request.POST["category"]] = request.POST["subCategory1"]
        else:
            categorySubCategoryMapList = dict( (key, value.split(", ")) for key, value in dict([ item.replace("]", "").split(": ") for item in obj[4].replace("{", "").replace("}", "").replace("'", "").replace("[", "").split("], ") ]).items())
            
            if categorySubCategoryMapList.__contains__(request.POST["category"]):
                if request.POST["subCategory1"] not in categorySubCategoryMapList[request.POST["category"]]:
                    categorySubCategoryMapList[request.POST["category"]].append(request.POST["subCategory1"])
            else:
                categorySubCategoryMapList[request.POST["category"]] = [request.POST["subCategory1"]]

        for obj in tickerTable.objects.all():
            obj.categorySubCategoryMapList = str(categorySubCategoryMapList)
            obj.save()    
    
        #print("categorySubCategoryMapList::", categorySubCategoryMapList)


    
def updateTikerTableTicker(request, dataList):

    dataListSet = [ item.split("|")[0] for item in dataList]

    print("Before tickerTable.objects.all()::", tickerTable.objects.all())
    
    for obj in tickerTable.objects.values_list():
        dbCommonDataList = []
        tickerList = []
        if obj[1] == "[]":
            dbCommonDataList = dataListSet
        else:
            tickerList = [ item.split("|")[0] for item in obj[1].replace("[", "").replace("]", "").replace("'", "").split(", ")]
            dbCommonDataList = list(set(tickerList + dataListSet))

        #print("obj::", obj)
        print("obj[3]::", obj[3])
        categoryTickerMapList = {}
        productsTablePrimary_ = productsTablePrimary.objects.filter(modelNumber=request.POST["productId"])[0]
        if obj[3] == "{}":
            categoryTickerMapList[productsTablePrimary_.category] = dbCommonDataList
            print("IF categoryTickerMapList::", categoryTickerMapList)
        else:
            categoryTickerMapList = dict( (key, value.split(", ")) for key, value in dict([ item.replace("]", "").split(": ") for item in obj[3].replace("{", "").replace("}", "").replace("'", "").replace("[", "").split("], ") ]).items())
            
            if categoryTickerMapList.__contains__(productsTablePrimary_.category):
                categoryTickerMapList[productsTablePrimary_.category] = list(set(categoryTickerMapList[productsTablePrimary_.category] + dbCommonDataList))

            else:
                categoryTickerMapList[productsTablePrimary_.category] = dbCommonDataList

        print("After tickerTable.objects.all()::", tickerTable.objects.all())
        for obj in tickerTable.objects.all():
            obj.tickerList = dbCommonDataList
            obj.categoryTickerMapList = str(categoryTickerMapList)
            obj.save()

def handleProductsTableSecodary(request):
    #print("handleProductsTableSecodary 1 request.POST::", request.POST)
    
    dataList = []
    counter = 0
    for index in ["%d" %i for i in range(1,16)]:
        if(request.POST[index + "_Value"] != ""):
            dataList.append(request.POST[index + "_Name"] + "|" + request.POST[index + "_Value"])
            counter = counter + 1

    updateTikerTableTicker(request, dataList)
    
    #print("handleProductsTableSecodary 2")
    for index in ["%d" %i for i in range(counter, 16)]:
        dataList.append("")

    #print("handleProductsTableSecodary 3")
    if request.POST.__contains__("productId"):
        #print("handleProductsTableSecodary 4")
        _productsTableSecodary =  productsTableSecodary(productId=request.POST["productId"], 
                otherFeature_1=dataList[0], otherFeature_2=dataList[1], otherFeature_3=dataList[2], 
                otherFeature_4=dataList[3], otherFeature_5=dataList[4], otherFeature_6=dataList[5], 
                otherFeature_7=dataList[6], otherFeature_8=dataList[7], otherFeature_9=dataList[8], 
                otherFeature_10=dataList[9], otherFeature_11=dataList[10], otherFeature_12=dataList[11], 
                otherFeature_13=dataList[12], otherFeature_14=dataList[13], otherFeature_15=dataList[14])
        #print("handleProductsTableSecodary 5")
        
        _productsTableSecodary.save()
        
        #print("handleProductsTableSecodary 6")

        return request, "hoverImages", request.POST["productId"]

    else:
        print("handleProductsTableSecodary 7")
        return request, "hoverImages", ""


def alterProductManagePOST(request):
    print("alterProductManagePOST POST::", request.POST)

    if request.POST["formAddProductAction"] == "alterData":
        if request.POST.__contains__("redirect"):
            print("alterData 1")
            return request, request.POST["redirect"], ""
        elif request.POST["action"] == "homeSlider":  #todo work painding
            print("alterData 2")
            form = HomeSliderImageTableForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return request, "home", ""
            else:
                print("error::form invalid:: HomeSliderImageTableForm")
        elif request.POST["action"] == "homeImages": #todo work painding
            print("alterData 3")
            form = HomeProductListImagesTableForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                updateTikerTableCategoryList(request)
                return request, "home", ""
            else:
                print("error::form invalid:: HomeProductListImagesTableForm")
        elif request.POST["action"] == "productIndex": 
            print("alterData 4") 
            return request, "alterProduct", ""
        elif request.POST["action"] == "payment":  #todo work painding
            print("alterData 5")
            if request.POST["modeOfPayment"] == "UPI":
                print("-------->", bool(request.POST["modeOfPayment"]))
                paymentTable_ = paymentTable(modeOfPayment=request.POST["modeOfPayment"], 
                        isActive=bool(request.POST["modeOfPayment"]), upiId=request.POST["upiId"], 
                        bankName="", ifscCode="", accountNumber="", benificiaryName="")
                paymentTable_.save()
            elif request.POST["modeOfPayment"] == "ACCOUNT":
                paymentTable_ = paymentTable(modeOfPayment=request.POST["modeOfPayment"], 
                            isActive=bool(request.POST["modeOfPayment"]), upiId="", bankName=request.POST["bankName"],
                            ifscCode=request.POST["ifscCode"], accountNumber=request.POST["accountNumber"], 
                            benificiaryName=request.POST["benificiaryName"])
                paymentTable_.save()
            else:
                print("alterData 5::ERROR") 
            return request, "payment", ""
        elif request.POST["action"] == "promocode":  #todo work painding
            print("alterData 6") 
            return request, "promocode", ""
        elif request.POST["action"] == "reviewAndRating":  #todo work painding
            print("alterData 7") 
            return request, "reviewAndRating", ""

    elif request.POST["formAddProductAction"] == "alterProduct":
        print("alterProduct 1") 
        if request.POST["action"] == "add":
            print("alterProduct 2")
            return request, "primaryDetails", ""
        elif request.POST["action"] == "update": #todo work painding
            print("alterProduct 3")
            return request, "update", ""
        elif request.POST["action"] == "view":  #todo work painding
            print("alterProduct 4")
            return request, "view", ""

    elif request.POST["formAddProductAction"] == "primaryDetails":
        print("primaryDetails 1")
        if not productsTablePrimary.objects.filter(modelNumber=request.POST["modelNumber"]).exists():
            print("primaryDetails 2")
            form = ProductsTablePrimaryForm(request.POST, request.FILES)
            print("primaryDetails 3")
            if form.is_valid():
                form.save()
                updateTikerTableCategorySubCategoryMapList(request)
            
                print("primaryDetails 4::", request.POST["modelNumber"])
                return request, "moreDetails", request.POST["modelNumber"]
            else:
                print("error::form invalid:: add Product primaryDetails")
        else:
            print("primaryDetails 5")
            messages.info(request, ("modelNumber:- '"+ request.POST["modelNumber"] +"' already exist"))
            return request, "primaryDetails", request.POST["modelNumber"]
        
        
    elif request.POST["formAddProductAction"] == "moreDetails":
        if (request.POST.__contains__("skip") and request.POST["skip"] == "skip"):
            print("moreDetails 1")
            return request, "hoverImages", request.POST["productId"]
        else:
            print("moreDetails 2")
            return handleProductsTableSecodary(request)
            
    elif request.POST["formAddProductAction"] == "hoverImages":
        if (request.POST.__contains__("skip") and request.POST["skip"] == "skip"):
            print("hoverImages 1")
            return request, "descriptionAndSpacificationManage", request.POST["productId"]
        else:
            print("hoverImages 2")
            form = ProductsTableTernaryForm(request.POST, request.FILES)
            print("hoverImages 3")
            if form.is_valid():
                form.save()
                print("hoverImages 4")
                return request, "descriptionAndSpacificationManage", request.POST["productId"]
            else:
                print("error::form invalid:: add Product hoverImages")

    elif request.POST["formAddProductAction"] == "descriptionAndSpacificationManage":
        if (request.POST.__contains__("skip") and request.POST["skip"] == "skip"):
            print("descriptionAndSpacificationManage 1")
            messages.info(request, ("modelNumber:- '"+ request.POST["productId"] +"' saved"))
            return request, "home", request.POST["productId"]
        else:
            print("descriptionAndSpacificationManage 2")
            productsTableQuaterly_ = productsTableQuaterly(productId=request.POST["productId"], 
                                        description=request.POST["description"], 
                                        specifications=request.POST["specifications"])
            productsTableQuaterly_.save()
            messages.info(request, ("modelNumber:- '"+ request.POST["productId"] +"' saved"))
            return request, "home", request.POST["productId"]



def handleSearchBox(request):
    print("handleSearchBox 1")
    searchProductTitle = request.POST["searchData"]
    if searchProductTitle != "" :
        print("handleSearchBox 1 if searchProductTitle::",searchProductTitle)
        #searchProductTitle = searchProductTitle.replace(" ", "").lower()
        #print("searchProductTitle::", searchProductTitle)
        productproductTitleListObj  =  productsTablePrimary.objects.filter(searchTitle__contains=searchProductTitle.replace(" ", "").lower())
        print("handleSearchBox 1 if productproductTitleListObj::",productproductTitleListObj)
        if len(productproductTitleListObj) != 0:
            url = "/product/search/" + searchProductTitle
            print("handleSearchBox 1 if url::",url)
            return url, "", ""
        else:
            print("handleSearchBox 1 else")
            #todo add some page when search item not present in our database
            relaventSearch  = "2"
            url = "/product/search/" + relaventSearch
            return url, searchProductTitle, relaventSearch
    else:
        print("handleSearchBox 2 else request.POST::",request.POST)
        return "", "", ""
