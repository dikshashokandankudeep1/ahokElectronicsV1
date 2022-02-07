from django.contrib import messages
from .models import productsTablePrimary, productsTableSecodary, productsTableQuaterly, paymentTable

from .forms import ProductsTablePrimaryForm, ProductsTableTernaryForm, HomeSliderImageTableForm, \
        HomeProductListImagesTableForm


def alterProductManagePOST(request):

    def handleProductsTableSecodary(request):
        print("handleProductsTableSecodary 1 request.POST::", request.POST)
        
        dataList = []
        counter = 0
        for index in ["%d" %i for i in range(1,16)]:
            if(request.POST[index + "_Value"] != ""):
                dataList.append(request.POST[index + "_Name"] + "|" + request.POST[index + "_Value"])
                counter = counter + 1
        
        print("handleProductsTableSecodary 2")
        for index in ["%d" %i for i in range(counter, 16)]:
            dataList.append("")

        print("handleProductsTableSecodary 3")
        if request.POST.__contains__("productId"):
            print("handleProductsTableSecodary 4")
            _productsTableSecodary =  productsTableSecodary(productId=request.POST["productId"], 
                    otherFeature_1=dataList[0], otherFeature_2=dataList[1], otherFeature_3=dataList[2], 
                    otherFeature_4=dataList[3], otherFeature_5=dataList[4], otherFeature_6=dataList[5], 
                    otherFeature_7=dataList[6], otherFeature_8=dataList[7], otherFeature_9=dataList[8], 
                    otherFeature_10=dataList[9], otherFeature_11=dataList[10], otherFeature_12=dataList[11], 
                    otherFeature_13=dataList[12], otherFeature_14=dataList[13], otherFeature_15=dataList[14])
            print("handleProductsTableSecodary 5")
            _productsTableSecodary.save()
            print("handleProductsTableSecodary 6")

            return request, "hoverImages", request.POST["productId"]

        else:
            print("handleProductsTableSecodary 7")
            return request, "hoverImages", ""

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
            return request, "descriptionAndSpacificationManage", ""
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
                    description=request.POST["description"], specifications=request.POST["specifications"])
            productsTableQuaterly_.save()
            messages.info(request, ("modelNumber:- '"+ request.POST["productId"] +"' saved"))
            return request, "home", request.POST["productId"]



def handleSearchBox(request):
    print("handleSearchBox 1")
    searchProductTitle = request.POST["searchData"]
    if searchProductTitle != "" :
        print("handleSearchBox 1 if searchProductTitle::",searchProductTitle)
        productproductTitleListObj  =  productsTablePrimary.objects.filter(filter_type='NO-FILTER').filter(title__contains=searchProductTitle)
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
