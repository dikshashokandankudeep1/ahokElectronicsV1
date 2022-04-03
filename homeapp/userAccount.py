from django.shortcuts import render
from .models import usertable, userordertable, userAddressBook
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .commom import toCamelCase, toCommaSeperatedCurrency
from .helper import searchContentInSearchBar, getUserId, getAddToCartData, getUserName, checkUserLogged

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


def orders_Helper(userordertable_list):
    print("userordertable_list::", userordertable_list)
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
        #warning = 0
        if userordertable_.paidAmount < userordertable_.finalPaidAmount:
            payAtHome = userordertable_.finalPaidAmount - userordertable_.paidAmount


        dataDict = { "orderPlacedDate"  : userordertable_.orderPlacedDate, 
                    "finalPaidAmount"   : toCommaSeperatedCurrency(userordertable_.finalPaidAmount),
                    #"onOrderPaidAmount" : userordertable_.onOrderPaidAmount, 
                    "payAtHome"         : toCommaSeperatedCurrency(payAtHome), 
                    #"warning"           : warning,
                    "orderDeliveryAddressHeading"   : orderDeliveryAddressHeading, 
                    "orderDeliveryAddressRestPart"  : orderDeliveryAddressRestPart,
                    "orderId" : userordertable_.orderId, 
                    "orderTrackingStatus" : orderTrackingStatus, 
                    "reason"    : reason,
                    "orderPaymentDate" : userordertable_.orderFirstPaymentDate, 
                    "orderedItemImage" : userordertable_.orderedItemImage,
                    "orderTitle"    : userordertable_.orderTitle, 
                    "orderItemId"   : userordertable_.orderItemId, 
                    "orderSellingQuantity" : userordertable_.orderSellingQuantity
        }
        productDictList.append(dataDict)

    dataDictionary = {}
    if len(productDictList) == 0:
        ordernotplaced = "Order Not Placed"
        dataDictionary = { "productDictList" : productDictList, "ordernotplaced" : ordernotplaced }
    else:
        dataDictionary = { "productDictList" : productDictList }

    return dataDictionary

def orders_View(request):

    print("IN orders_View")
    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    if request.method == "POST":
        print("orders_View 0 request.POST", request.POST)
        if(request.POST.__contains__("search")):
            return searchContentInSearchBar(request)

    userordertable_list = userordertable.objects.filter(userId=request.user.id)
    print("orders_View 1 userordertable_list::",userordertable_list)
    
    dataDictionary = orders_Helper(userordertable_list)

    print("orders_View 2 dataDictionary::", dataDictionary)
    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
        'headerDict'          : headerDict,
        "dataDictionary"      : dataDictionary
    }
    return render(request, "user/orders/index.html", context)


def Product_viewMore_view(request, orderId):

    print("IN Product_viewMore_view")
    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    userordertable_list = userordertable.objects.filter(userId=request.user.id).filter(orderId=orderId)
    print("orders_View 1 userordertable_list::",userordertable_list)
    
    dataDictionary = orders_Helper(userordertable_list)

    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
        'headerDict'          : headerDict,
        "dataDictionary"      : dataDictionary
    }
    return render(request, "user/orders/viewMore/index.html", context)



def account_profileInformation_View(request):

    isNotLogged = checkUserLogged(request, request.get_full_path())
    if isNotLogged:
        return redirect(isNotLogged)

    return account_View(request, "profileinformation")

def account_View(request, touds):

    if touds == "orders":
        return orders_View(request)
    
    userObjects = usertable.objects.filter(userId=request.user.id)
    userObject = userObjects[0]

    postOperation = []
    if request.method == "POST":
        print("I AM IN POST::", request.POST)
        if request.POST.__contains__("menuSwitch"):
            if request.POST["menuSwitch"] == "profileinformation":
                return redirect("/account")
            elif request.POST["menuSwitch"] == "manageaddresses":
                return redirect("/account/addresses")
            else:
                url = "/account/" + request.POST["menuSwitch"]
                return redirect(url)
        else:
            if request.POST.__contains__("buttonOperation"):
                splitData = request.POST["buttonOperation"].split(":")
                print("buttonOperation::", splitData)
                if splitData[0] == "manageAddresses":
                    if splitData[1] != "addormodifyaddress":
                        postOperation = splitData
                    else:
                        postOperation = (splitData + list(request.POST))
                        
                elif splitData[0] == "profileinformation":
                    if splitData[1] == "personaInfo":
                        postOperation = {   "personaInfo" : 
                                            {
                                                "firstName" : request.POST["firstName"],
                                                "lastName" : request.POST["lastName"],
                                                "gender" : request.POST["gender"]
                                            }
                                        }
                    elif splitData[1] == "emailAddress":
                        postOperation = {   "emailAddress" : 
                                            {
                                                "emailAddress" : request.POST["emailAddress"]
                                            }
                                        }
                    else: #splitData[1] == "contactNumber"
                        postOperation = {   "contactNumber" : 
                                            {
                                                "mobileNumber" : request.POST["mobileNumber"],
                                                "whatsappNumber" : request.POST["whatsappNumber"]
                                            }
                                        }

                elif splitData[0] == "changepassword":
                    if userObject.password == request.POST["currentPassword"]:
                        for userObj in userObjects:
                            userObj.password = request.POST["newPassword"]
                            userObj.save()
                        userObject = userObjects[0]
                        messages.set_level(request, messages.INFO)
                        messages.info(request, "password update successful")
                    else:
                        messages.set_level(request, messages.ERROR)
                        messages.error(request, "current password mismatch please try again...")
            else:
                print("manageAddresses:buttonOperation::ELSE")
                pass

    dataShow = ""
    dataDictionary = {}
    
    
    print("account_View 0 userObject::", userObject)


    print("account_View touds::", touds)
    if touds =="profileinformation":
        
        if postOperation:
            if postOperation.__contains__("personaInfo"):
                for userObj in userObjects:
                    userObj.firstName       =   postOperation["personaInfo"]["firstName"]
                    userObj.lastName        =   postOperation["personaInfo"]["lastName"]
                    userObj.gender          =   postOperation["personaInfo"]["gender"]
                    userObj.save()

            elif postOperation.__contains__("emailAddress"):
                for userObj in userObjects:
                    userObj.emailAddress    =   postOperation["emailAddress"]["emailAddress"]
                    userObj.save()
            
            else:#postOperation has key == "contactNumber"
                for userObj in userObjects:
                    userObj.mobileNumber    =   postOperation["contactNumber"]["mobileNumber"]
                    userObj.whatsappNumber  =   postOperation["contactNumber"]["whatsappNumber"]
                    userObj.save()
            userObject = userObjects[0]

        dataDictionary = {"userId" : userObject.userId, "username" : userObject.username, "firstName" : userObject.firstName, 
                            "lastName" : userObject.lastName, "gender" : userObject.gender, "emailAddress" : userObject.emailAddress,
                            "mobileNumber" : userObject.mobileNumber, "whatsappNumber" : userObject.whatsappNumber }
        dataShow = touds
    elif touds =="addresses":
        manageAddressesDict = []
        oldOperation = ""
        editDict = {"firstName" : "", "lastName": "", "mobileNumber" : "", "emailAddress": "", 
                    "address" : "", "townOrCity" : "", "state": "", "pincode": "", 
                    "country": "", "landmark": "", "locationType": "Home"}
        
        if (userObject.userAddressBooks != "") and (userObject.userAddressBooks != "[]"):
            userAddressBookList = list(map(int, userObject.userAddressBooks.strip('][').split(', ')))
        else:
            userAddressBookList = []

        if postOperation:
            if postOperation[1] == "edit": #click on edit address
                addressObjs = userAddressBook.objects.filter(userId=request.user.id).filter(id=int(postOperation[2]))
                oldOperation = int(postOperation[2])
                for addressObj in addressObjs:
                    editDict["id"]              = int(postOperation[2])
                    editDict["firstName"]       = addressObj.firstName
                    editDict["lastName"]        = addressObj.lastName
                    editDict["mobileNumber"]    = addressObj.phoneNo
                    editDict["emailAddress"]    = addressObj.emailAddress
                    editDict["address"]         = addressObj.address
                    editDict["townOrCity"]      = addressObj.townOrCity
                    editDict["state"]           = addressObj.state
                    editDict["pincode"]         = addressObj.postcodeOrZIP
                    editDict["country"]         = addressObj.country
                    editDict["landmark"]        = addressObj.landmark
                    editDict["locationType"]        = addressObj.locationType
                print("EDIT::", manageAddressesDict)
            elif postOperation[1] == "delete": #click on delete address
                userAddressBookList.remove(int(postOperation[2]))
                for u_obj in userObjects:
                    u_obj.userAddressBooks = str(list(set(userAddressBookList)))
                    u_obj.save()
                userObject = userObjects[0]
                print("After delete userAddressBookList::", userAddressBookList)
            else:#addormodifyaddress
                if request.POST["id"] == "":  #Modify address
                    userAddressBook_ = userAddressBook(userId=request.user.id, firstName=toCamelCase(request.POST["firstName"]), 
                                        lastName=toCamelCase(request.POST["lastName"]), locationType=request.POST["locationType"],
                                        address=toCamelCase(request.POST["address"]), landmark=toCamelCase(request.POST["landmark"]), 
                                        townOrCity=request.POST["townOrCity"], state=request.POST["state"], 
                                        country=toCamelCase(request.POST["country"]), postcodeOrZIP=request.POST["pincode"], 
                                        phoneNo=request.POST["mobileNumber"], emailAddress=request.POST["emailAddress"].lower(), 
                                        orderNotes="")
                else: #add new address
                    userAddressBook_ = userAddressBook(id=int(request.POST["id"]), userId=request.user.id, firstName=toCamelCase(request.POST["firstName"]), 
                                        lastName=toCamelCase(request.POST["lastName"]), locationType=request.POST["locationType"],
                                        address=toCamelCase(request.POST["address"]), landmark=toCamelCase(request.POST["landmark"]), 
                                        townOrCity=request.POST["townOrCity"], state=request.POST["state"], 
                                        country=toCamelCase(request.POST["country"]), postcodeOrZIP=request.POST["pincode"], 
                                        phoneNo=request.POST["mobileNumber"], emailAddress=request.POST["emailAddress"].lower(), 
                                        orderNotes="")
                userAddressBook_.save()
                userAddressBookList.append(userAddressBook_.id)
                for u_obj in userObjects:
                    u_obj.userAddressBooks = str(list(set(userAddressBookList)))
                    u_obj.save()
                userObject = userObjects[0]
                
            if (userObject.userAddressBooks != "") and (userObject.userAddressBooks != "[]"):
                userAddressBookList = list(map(int, userObject.userAddressBooks.strip('][').split(', ')))
            else:
                userAddressBookList = []
            for address in userAddressBookList:
                if oldOperation and oldOperation != address:  #ignore other address when click on edit
                    continue
                addressObjs = userAddressBook.objects.filter(userId=request.user.id).filter(id=address)
                for addressObj in addressObjs:
                    dictData = {    "id" : addressObj.id,
                                    "fullName": (addressObj.firstName + " " + addressObj.lastName  ),
                                    "mobileNumber" : addressObj.phoneNo,
                                    "address" : (addressObj.address.lower() + ", " + addressObj.landmark.lower() + ", " +
                                                addressObj.townOrCity + ", " + addressObj.state + " - " + addressObj.postcodeOrZIP)
                                }
                    manageAddressesDict.append(dictData)
        
        dataDictionary = {"username" : userObject.username, 
                            "manageAddressesDict" : manageAddressesDict, 
                            "oldOperation" :  oldOperation,
                            "editDict" : editDict}
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
    headerDict = {"userID" : getUserId(request), "username" : getUserName(request), "addToCartButtonDict" : getAddToCartData(request)}
    context = {
       'headerDict'          : headerDict, 
       "dataShow"            : dataShow,
       "dataDictionary"      : dataDictionary
    }
    return render(request,"user/account/index.html", context)
