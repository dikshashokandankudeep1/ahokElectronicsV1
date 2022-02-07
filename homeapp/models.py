from django.db import models

class paymentTable(models.Model):
    modeOfPayment   = models.CharField(blank = True, max_length=50, default="")
    isActive        = models.BooleanField(blank=True, default=True)
    upiId           = models.CharField(blank = True, max_length=50, default="")
    bankName        = models.CharField(blank = True, max_length=50, default="")
    ifscCode        = models.CharField(blank = True, max_length=50, default="")
    accountNumber   = models.CharField(blank = True, max_length=50, default="")
    benificiaryName = models.CharField(blank = True, max_length=50, default="")

    def isUpi(this):
        if this.modeOfPayment == "UPI":
            return True
        else:
            return False

    def isAccountNumber(this):
        if this.modeOfPayment == "ACCOUNT":
            return True
        else:
            return False

class promoCodes(models.Model):
    promoCodeId             = models.CharField(blank = True, max_length=50, default="")
    isActive                = models.BooleanField(blank=True, default=True)
    discountPercentage      = models.IntegerField(blank=True, null=True, default=0)
    minSellingPriceCritaria = models.IntegerField(blank=True, null=True, default=0) 
    maxSellingPriceCriteria = models.IntegerField(blank=True, null=True, default=0)
    newUserDiscountFlag     = models.BooleanField(blank=True, default=True)
    onSaleFlag              = models.BooleanField(blank=True, default=True)
    saleOccasion            = models.CharField(blank = True, max_length=50, default="")

class homeSliderImageTable(models.Model):
    image                  = models.ImageField(blank=True, null=True)
    isActive               = models.BooleanField(blank=True, default=True)
    productRedirectUrl     = models.CharField(blank = True, max_length=50, default="")
    description            = models.CharField(blank = True, max_length=50, default="")

class homeProductListImagesTable(models.Model):
    image       = models.ImageField(blank=True, null=True)
    isActive    = models.BooleanField(blank=True, default=True)
    category    = models.CharField(blank = True, max_length=50, default="")

class reviewAndRatingTable(models.Model):
    userId              =   models.CharField(blank = True, max_length=50, default="")
    productId           =   models.CharField(blank = True, max_length=50, default="")
    description         =   models.CharField(blank = True, max_length=50, default="")
    rating              =   models.IntegerField(blank=True, null=True, default=0)
    image_1             =   models.ImageField(blank=True, null=True)
    image_2             =   models.ImageField(blank=True, null=True)
    date                =   models.DateField(blank=True, null=True)

class productsTableQuaterly(models.Model):
    productId       =   models.CharField(blank=True, max_length=50, default="")
    description     =   models.CharField(blank=True, max_length=500, default="")
    specifications  =   models.CharField(blank=True, max_length=1000, default="")
    
    #Highlights , Seller, DeliveryAreaPinCodes, 
    # Specifications[ General , Video Features, Audio Features, Smart Tv Features, Connectivity Features, 
    #                   Power Features, Dimensions, Warranty, Installation & Demo, Note ]
    # https://www.flipkart.com/samsung-crystal-4k-pro-146-cm-58-inch-ultra-hd-4k-led-smart-tv-voice-search/p/itm47c29d0aea456?pid=TVSG2CG7NHA8C5HP&lid=LSTTVSG2CG7NHA8C5HPX8BJWB&marketplace=FLIPKART&fm=neo%2Fmerchandising&iid=M_2626083a-d819-4780-9f15-41862ed2a42d_2_UA5V2KMY7BBY_MC.TVSG2CG7NHA8C5HP&ppt=dynamic&ppn=LOYALTY_PAGE&ssid=arlyj2u6r40000001639652681253&otracker=clp_pmu_v2_Big%2BScreen%2BTVs_2_2.productCard.PMU_V2_SAMSUNG%2BCrystal%2B4K%2BPro%2B146%2Bcm%2B%252858%2Binch%2529%2BUltra%2BHD%2B%25284K%2529%2BLED%2BSmart%2BTV%2Bwith%2BVoice%2BSearch_television-store_TVSG2CG7NHA8C5HP_neo%2Fmerchandising_1&otracker1=clp_pmu_v2_PINNED_neo%2Fmerchandising_Big%2BScreen%2BTVs_LIST_productCard_cc_2_NA_view-all&cid=TVSG2CG7NHA8C5HP


class productsTableTernary(models.Model):
    productId       =   models.CharField(blank=True, max_length=50, default="")
    hoverImage_1    =   models.ImageField(blank=True, null=True)
    hoverImage_2    =   models.ImageField(blank=True, null=True)
    hoverImage_3    =   models.ImageField(blank=True, null=True)
    hoverImage_4    =   models.ImageField(blank=True, null=True)
    hoverImage_5    =   models.ImageField(blank=True, null=True)
    hoverImage_6    =   models.ImageField(blank=True, null=True)

    def getHoverImageDict(self):
        hoverImageDict = {}
        if self.hoverImage_1 != "":
            hoverImageDict[1] = self.hoverImage_1.url
        if self.hoverImage_2 != "":
            hoverImageDict[2] = self.hoverImage_2.url
        if self.hoverImage_3 != "":
            hoverImageDict[3] = self.hoverImage_3.url
        if self.hoverImage_4 != "":
            hoverImageDict[4] = self.hoverImage_4.url
        if self.hoverImage_5 != "":
            hoverImageDict[5] = self.hoverImage_5.url
        if self.hoverImage_6 != "":
            hoverImageDict[6] = self.hoverImage_6.url
        return hoverImageDict


class productsTableSecodary(models.Model):
    productId       =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_1  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_2  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_3  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_4  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_5  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_6  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_7  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_8  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_9  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_10  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_11  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_12  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_13  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_14  =   models.CharField(blank=True, max_length=50, default="")
    otherFeature_15  =   models.CharField(blank=True, max_length=50, default="")


class productsTablePrimary(models.Model):
    modelNumber     =   models.CharField(blank=True, max_length=50, default="", primary_key=True)
    category        =   models.CharField(blank = True, max_length=50, default="")
    subCategory     =   models.CharField(blank = True, max_length=50, default="")
    brandName       =   models.CharField(blank = True, max_length=50, default="")
    title           =   models.CharField(blank = True, max_length=50, default="")
                        #title => brandName + category + subCategory + otherthings + (ModelNumber)
    price           =   models.IntegerField(blank=True, null=True, default=0)
    quantity        =   models.IntegerField(blank=True, null=True, default=0)
    warranty        =   models.CharField(blank=True, max_length=50, default="")
    mainImage       =   models.ImageField(blank=True, null=True)

    userRatings     =   models.IntegerField(blank=True, null=True, default=0)
    reviewList      =   models.CharField(blank=True, max_length=50, default="")
    #onsale          =   models.BooleanField(blank=True, default=True)
    

class userAddressBook(models.Model):
    userId          =   models.CharField(blank = True, max_length=50, default="")
    firstName       =   models.CharField(blank = True, max_length=50, default="")
    lastName        =   models.CharField(blank = True, max_length=50, default="")
    companyName     =   models.CharField(blank = True, max_length=50, default="")
    countryOrRegion =   models.CharField(blank = True, max_length=50, default="")
    streetAddress1  =   models.CharField(blank = True, max_length=50, default="")#House No or street name
    streetAddress2  =   models.CharField(blank = True, max_length=50, default="")#Apartment, suit, unit, etc. (optional)
    townOrCity      =   models.CharField(blank = True, max_length=50, default="")
    stateOrCounty   =   models.CharField(blank = True, max_length=50, default="")
    postcodeOrZIP   =   models.CharField(blank = True, max_length=50, default="")
    phoneNo         =   models.CharField(blank = True, max_length=50, default="")
    emailAddress    =   models.CharField(blank = True, max_length=50, default="")
    orderNotes      =   models.CharField(blank = True, max_length=50, default="")

class userordertable(models.Model):
    userId                  =   models.IntegerField(blank=True, null=True, default=0)
    orderDeliveryAddress    =   models.CharField(blank=True, max_length=50, default="")
    orderId                 =   models.CharField(blank=True, max_length=50, default="")
                                #userID - orderGroup.id(currenttime with AM PM) - userordertable.id
    typeofpayment           =   models.BooleanField(blank=True, default=True)   #0-half and 1-full payment

    orderFirstPaidTrxnID            =   models.CharField(blank = True, max_length=50, default="")
    orderSecondPaidTrxnID           =   models.CharField(blank = True, max_length=50, default="")

    orderFirstPaymentID     =   models.CharField(blank = True, max_length=50, default="")
    orderSecondPaymentID    =   models.CharField(blank = True, max_length=50, default="")

    orderPlacedDate                 =   models.DateField(blank=True, null=True)
    orderEstimatedArrivalDateStart  =   models.DateField(blank=True, null=True)
    orderEstimatedArrivalDateEnd    =   models.DateField(blank=True, null=True)
    orderFirstPaymentDate           =   models.DateField(blank=True, null=True)  #partial paid date if partial paid
    orderSecondPaymentDate          =   models.DateField(blank=True, null=True)  #rest amount paid date if partial paid

    orderItemId                     =   models.CharField(blank = True, max_length=50, default="")
    orderTitle                      =   models.CharField(blank=True, max_length=50, default="")
    orderedItemImage                =   models.ImageField(blank=True, null=True)
    orderSellingPricePerItem        =   models.IntegerField(blank=True, null=True, default=0)
    orderSellingQuantity            =   models.IntegerField(blank=True, null=True, default=0)

    onOrderPaidAmount               =   models.IntegerField(blank=True, null=True, default=0) #initial paid amount
    paidAmount                      =   models.IntegerField(blank=True, null=True, default=0) #current paid
    finalPaidAmount                 =   models.IntegerField(blank=True, null=True, default=0) #totalprice - discount

    orderDeliveryCharge             =   models.IntegerField(blank=True, null=True, default=0)
    orderDiscountCouponId           =   models.IntegerField(blank=True, null=True, default=0)

    orderTrackingStatus             =   models.IntegerField(blank=True, null=True, default=0)
    #0 user just Orderd admin check transactionID
    #1 Packing started [HP]
    #2 Packing started [FP]
    #3 Packed [HP]
    #4 Packed [FP]
    #5 Delivery started [HP]
    #6 Delivery started [FP]
    #7 Out for delivery:Picked by courier guy [HP]
    #8 Out for delivery:Picked by courier guy [FP]
    #9 Delivery guy on the way [HP]
    #10 Delivery guy on the way [FP]
    #11 Guy reached on delivery location [HP]
    #12 Guy reached on delivery location [FP]
    #13 Not deliverd to the customer not paid rest amount or cancel order [HP]
    #14 Deliverd to the customer with paid rest amount [HP]
    #15 Deliverd to the customer [FP]
    #16 canceled by admin:Due to wrong transaction ID [HP]
    #17 canceled by admin:due to wrong transaction ID [FP]
    #18 canceled by admin:product out of stock [HP]
    #19 canceled by admin:product out of stock [FP]
    #20 canceled by user, from::before delivery started Payment [HP]
    #21 canceled by user, from::before delivery started Payment [FP]
    #22 returned by user, from::door-step Payment [HP]
    #23 returned by user, from::door-step Payment [FP]
    #24 returned by user, from::after delivered::with delivery charge [FP][W-DC]
    #25 returned by user, from::after delivered::except delivery charge [FP][E-DC]

class userOrderGrouptable(models.Model):
    userId         =   models.IntegerField(blank=True, null=True, default=0)
    ordersList     =   models.CharField(blank = True, max_length=500, default="")
    
    #orderGroupUserAdminStatus      =   models.IntegerField(blank=True, null=True, default=0)
    #0 order placed by user [HP]
    #1 order placed by user [FP]
    #2 canceled by admin:Due to wrong transaction ID [HP]
    #3 canceled by admin:due to wrong transaction ID [FP]
    #4 order confirmed by admin [HP]
    #5 order confirmed by admin [FP]
    #orderGroupTotalSellingAmount   =   models.IntegerField(blank=True, null=True, default=0)
                                        #Total Amount which Need to pay
    #orderGroupDepositAmount        =   models.IntegerField(blank=True, null=True, default=0)
                                        #First time paid amount when order placed
    #orderGroupUnpaidAmount         =   models.IntegerField(blank=True, null=True, default=0)
                                        #(Total Amount - Deposit Amount)
    #paymentInitialTrxnID           =   models.CharField(blank = True, max_length=50, default="")
                                        #orderGroupDepositAmount transaction ID
    #paymentSecondaryTrxnID         =   models.CharField(blank = True, max_length=50, default="")
                                        #if orderGroupUnpaidAmount => transactionId = orderGroupUnpaidAmount
                                        #else => transactionId = orderGroupDepositAmount




class usertable(models.Model):
    userId              =   models.CharField(blank = True, max_length=50, default="")
    isActive            =   models.BooleanField(blank=True, default=True)
    #userImage          =   models.ImageField(blank=True, null=True)   # user add profile picture
    firstName           =   models.CharField(blank = True, max_length=50, default="")
    lastName            =   models.CharField(blank = True, max_length=50, default="")
    username            =   models.CharField(blank = True, max_length=50, default="")
    password            =   models.CharField(blank = True, max_length=50, default="")
    mobilenumber        =   models.CharField(blank = True, max_length=50, default="")
    whatsappnumber      =   models.CharField(blank = True, max_length=50, default="")
    emailaddress        =   models.CharField(blank = True, max_length=50, default="")
    addToCartItemsDict  =   models.CharField(blank = True, max_length=200, default="")
    userAddressBooks    =   models.CharField(blank = True, max_length=200, default="")
    userOrderBooks      =   models.CharField(blank = True, max_length=200, default="")

    ordersList          =   models.CharField(blank = True, max_length=500, default="")
    wishList            =   models.CharField(blank = True, max_length=500, default="")
    reviewIdsList       =   models.CharField(blank = True, max_length=500, default="")

class messagetable(models.Model):
    senderId            =   models.IntegerField(blank=True, null=True, default=0)
    receverId           =   models.IntegerField(blank=True, null=True, default=0)
    messageContent      =   models.CharField(blank = True, max_length=50, default="")

