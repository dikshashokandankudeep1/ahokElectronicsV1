function showId(ID) {
    document.getElementById(ID).style.display = "block";
}

function hideId(ID) {
    document.getElementById(ID).style.display = "none";
}

function toCommaSeperatedCurrency(number){
    numberStr = number.toString()
    if(! numberStr.includes('.')){
        numberStr += ".00"    
    }
    
    return numberStr.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/*
function toCommaSeperatedCurrency(currency, flag="float"){
    let finalOutput = ""
    let currencySplit = currency.split(".")
    if(currencySplit[0].length <= 3){
        if (flag == "float"){
            if(currencySplit.length == 2){
                return currency;
            }
            else{
                return (currency + ".00")
            }
        }
        else{
            return (currencySplit[0] + ".00")
        }
    }
    else{
        let internalOutput = checkThreeDigit(currency);
        if(finalOutput == ""){
            finalOutput = internalOutput
        }
        else{
            finalOutput = finalOutput + "," + internalOutput
        }
        
        if (flag == "float"){
            if(currencySplit.length == 2){
                return (finalOutput + "." + currencySplit[1]);
            }
            else{
                return (finalOutput + ".00")
            }
        }
        else{
            return finalOutput;
        }
    }
    function checkThreeDigit(currency){
        let frontIntData = parseInt(currency.split(".")[0])
        if( frontIntData > 999 ){
            let innerStrSplit = ((frontIntData / 1000).toString()).split(".")
            let internalOutput =  checkThreeDigit(innerStrSplit[0].toString());
            if(finalOutput == ""){
                finalOutput = internalOutput
            }
            else{
                finalOutput = finalOutput + "," + internalOutput
            }
            return innerStrSplit[1];
        }
        else{
            if(parseInt(currency) > 99){
                let splitData = ((parseInt(currency) / 100).toString()).split(".");
                let output = splitData[0] + "," + splitData[1];
                return output;
            }
            else{
                return currency;
            }
        }
    }
}
*/
function commaSeperatedCurrencyToFloatOrInt(currency, flg="float"){
    let finalStr = ""
    for (var i = 0; i < currency.length; i++) {
        if(currency[i] != ','){
            if((currency[i] == '.') && (flg != "float")){
                break;
            }
            finalStr = finalStr + currency[i];
        }
    }
    return finalStr;
}

function testDemo1(){
    let currency = "9986386839.0877";
    let output = toCommaSeperatedCurrency(currency, "float")
    console.log("Input::", currency);
    console.log("Output::", output);
}

function testDemo2(){
    let currency = "5,89.0877";
    let output = commaSeperatedCurrencyToFloatOrInt(currency, "float")
    console.log("Input::", currency);
    console.log("Output::", output);
}