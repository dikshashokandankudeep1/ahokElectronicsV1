from django.shortcuts import render
from .models import usertable, userordertable
from .helper import searchContentInSearchBar
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth

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

def orders_View(request):
    if request.method == "POST":
        print("orders_View 0 request.POST", request.POST)
        if(request.POST.__contains__("search")):
            print("orders_View searchContent")
            return searchContentInSearchBar(request)

    print("orders_View 1 orders")

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
        "dataDictionary"      : dataDictionary
    }
    return render(request, "user/orders/index.html", context)



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
        print("I AM IN POST")
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
                          "firstname" : userObject.firstname, "lastname" : userObject.lastname,
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
