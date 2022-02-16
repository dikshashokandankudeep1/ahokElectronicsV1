from django.shortcuts import render
from .models import tickerTable
from .helper import alterProductManagePOST, getUserId

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
        "userID" : getUserId(request),
        "touds" : touds,
        "secondTouds" : secondTouds, 
        "productId" : productId,
        "categoryList" : categoryList,
        "tickerList" : tickerList
    }
    return render(request, "manager/index.html", context)
