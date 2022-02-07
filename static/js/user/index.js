function showId(ID) {
    console.log("ShowID:: ", ID);
    document.getElementById(ID).style.display = "block";
}

function hideId(ID) {
    console.log("HideID:: ", ID);
    document.getElementById(ID).style.display = "none";
}

window.onload = function() {

    //hideId('ProfileInformation_def');
    //hideId('ManageAddresses_onClick');

    hideId('personalInfo_name');
    hideId('personalInfo_gender');
    hideId('personalInfo_cancel');
    hideId('emailAddress_email');
    hideId('emailAddress_cancel');
    hideId('mobileNumber_mobile');
    hideId('mobileNumber_cancel');

    updateQuantityonPageLoad('{{dataDictionary.itemidList}}');

    hideId("SOMEITEMSELECTED");
    hideId("SELECTALLITEMS");
    showId("DESELECTALLITEMS");

    hideId("SUBTOTALBUTTON1");
    showId("SUBTOTALBUTTON2");
    hideId("SUBTOTALBUTTON3");
    showId("SUBTOTALBUTTON4");
};


function funcOnClickSubHeading(idType) {
    if ('ProfileInformation' == idType) {
        showId('ProfileInformation');
        hideId('ProfileInformation_def');
        hideId('ManageAddresses_onClick');
    }
}

function funcEdit(idType) {
    if ('personalInfo' == idType) {
        hideId('personalInfo_def_edit');
        hideId('personalInfo_def_name');
        hideId('personalInfo_def_gender');

        showId('personalInfo_name');
        showId('personalInfo_gender');
        showId('personalInfo_cancel');
    } else if ('emailAddress' == idType) {
        hideId('emailAddress_def_email');
        hideId('emailAddress_def_edit');
        showId('emailAddress_email');
        showId('emailAddress_cancel');

    } else if ('mobileNumber' == idType) {
        hideId('mobileNumber_def_mobile');
        hideId('mobileNumber_def_edit');
        showId('mobileNumber_mobile');
        showId('mobileNumber_cancel');
    }
}

function funcCancel(idType) {
    if ('personalInfo' == idType) {
        showId('personalInfo_def_edit');
        showId('personalInfo_def_name');
        showId('personalInfo_def_gender');
        hideId('personalInfo_name');
        hideId('personalInfo_gender');
        hideId('personalInfo_cancel');

    } else if ('emailAddress' == idType) {
        showId('emailAddress_def_email');
        showId('emailAddress_def_edit');
        hideId('emailAddress_email');
        hideId('emailAddress_cancel');

    } else if ('mobileNumber' == idType) {
        showId('mobileNumber_def_mobile');
        showId('mobileNumber_def_edit');
        hideId('mobileNumber_mobile');
        hideId('mobileNumber_cancel');
    }
}


function updateQuantityonPageLoad(itemidList) {
    for (index = 0; index < itemidList.length; index++) {
        if (parseInt(itemidList[index])) {
            hideId((itemidList[index]) + "_onclickchangeQuantity");
        }
    }
}

function changeProductQuantity() {
    document.getElementById("productQuantityTextbox").value = document.getElementById("productQuantityDropdown").value;
}

function changeUserComplains() {
    document.getElementById("userComplainsTextbox").innerHTML = document.getElementById("userComplainsDropdown").value;
}

function checkUncheckOrder(itemId, validateWith) {
    vect = [];
    if (document.getElementById("UNBUYSTORE").value !="[]") {
        vect = document.getElementById("UNBUYSTORE").value.replace("[","").replace("]","").split(",");
    }

    validationFlg = false
    if (validateWith == "TOGGLE") {
        validationFlg = document.getElementById("CHECK_" + itemId).checked;
    } else if (validateWith == "CHECK") {
        validationFlg = true;
        document.getElementById("CHECK_" + itemId).checked = true;
    } else {
        document.getElementById("CHECK_" + itemId).checked = false;
    }

    if (validationFlg) {
        for (var i = 0; i < vect.length; i++) {
            if (vect[i] === itemId) {
                vect.splice(i, 1);
            }
        }
        itemQuantPrice = document.getElementById(itemId + "_SUBTOTALIDINFO").value.split("/").map(iNum => parseInt(iNum, 10));
        subTotalQuantPricevec = document.getElementById("SUBTOTALQUANTPRICE").value.split("/").map(iNum => parseInt(iNum, 10));

        newSubTotalQuant = (subTotalQuantPricevec[0] + itemQuantPrice[0]);
        newSubTotalPrice = (subTotalQuantPricevec[1] + (itemQuantPrice[0] * itemQuantPrice[1]));
        STR ="Subtotal (" + newSubTotalQuant.toString() +" items): ₹<b>" + newSubTotalPrice.toString() +"</b>";
        document.getElementById('SUBTOTALBUTTON2').innerHTML = STR;
        document.getElementById('SUBTOTALBUTTON4').innerHTML = STR;
        document.getElementById('SUBTOTALQUANTPRICE').value = newSubTotalQuant.toString() +
            ' / ' + newSubTotalPrice.toString();
    } else {
        vect.push(itemId);
        itemQuantPrice = document.getElementById(itemId +"_SUBTOTALIDINFO").value.split("/").map(iNum => parseInt(iNum, 10));
        subTotalQuantPricevec = document.getElementById("SUBTOTALQUANTPRICE").value.split("/").map(iNum => parseInt(iNum, 10));
        newSubTotalQuant = (subTotalQuantPricevec[0] - itemQuantPrice[0]);
        newSubTotalPrice = (subTotalQuantPricevec[1] - (itemQuantPrice[0] * itemQuantPrice[1]));
        STR ="Subtotal (" + newSubTotalQuant.toString() +
           " items):₹ <b>" + newSubTotalPrice.toString() +"</b>";
        document.getElementById("SUBTOTALBUTTON2").innerHTML = STR;
        document.getElementById("SUBTOTALBUTTON4").innerHTML = STR;
        document.getElementById("SUBTOTALQUANTPRICE").value = newSubTotalQuant.toString() +"/" + newSubTotalPrice.toString();
    }
    document.getElementById("UNBUYSTORE").value = "[" + vect.toString() + "]";
    productDictListLength = '{{dataDictionary.productDictList|length}}';
    if (vect.length ==
        productDictListLength) {
        hideId("DESELECTALLITEMS");
        hideId("SELECTALLITEMS");
        showId("SOMEITEMSELECTED");
        hideId("SUBTOTALBUTTON2");
        showId("SUBTOTALBUTTON1");
        hideId("SUBTOTALBUTTON4");
        showId("SUBTOTALBUTTON3");
    } else if (!vect.length) {
        hideId("SOMEITEMSELECTED");
        hideId("SELECTALLITEMS");
        showId("DESELECTALLITEMS");
        hideId("SUBTOTALBUTTON1");
        showId("SUBTOTALBUTTON2");
        hideId("SUBTOTALBUTTON3");
        showId("SUBTOTALBUTTON4");
    } else {
        hideId("DESELECTALLITEMS");
        hideId("SOMEITEMSELECTED");
        showId("SELECTALLITEMS");
        hideId("SUBTOTALBUTTON1");
        showId("SUBTOTALBUTTON2");
        hideId("SUBTOTALBUTTON3");
        showId("SUBTOTALBUTTON4");
    }
}

function selectDeselect(validationType) {
    console.log("validationType::", validationType);
    itemidList
        = '{{dataDictionary.itemidList}}';
    console.log("itemidList::", itemidList);
    if (validationType == "DESELECTALLITEMS") {
        validateWith = "UNCHECK";
    } else {
        validateWith = "CHECK";
    }
    for (var i = 0; i <
        itemidList.length; i++) {
        if (parseInt(itemidList[i])) {
            checkUncheckOrder(itemidList[i], validateWith);
        }
    }
}

function noItemProceedToBuyButtonValidation(button) {
    if (document.getElementById("SUBTOTALQUANTPRICE").value == '0/0') {
        button.setCustomValidity(
            'Please select at least one item to Checkout');
    } else {
        button.setCustomValidity('');
    }
}
