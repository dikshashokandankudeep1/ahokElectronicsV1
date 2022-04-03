
def setSession(request, key, value):
    request.session[key] = value

def getSession(request, key):
    if request.session.__contains__(key):
        print("getSession key contains....",key, request.session[key])
        return request.session[key]
    else:
        print("getSession key not contains....")
        return ""

def toCamelCase(stringData):
    if stringData:
        vect = stringData.split(" ")
        outputString = ""
        for vec in vect:
            outputString += vec[0].upper() + vec[1:].lower() + " "
        return outputString.strip()
    else:
        return ""
def toCommaSeperatedCurrency(number):
    commaSeparatedCurrency = "{:,}".format(number)
    if '.' not in commaSeparatedCurrency:
        commaSeparatedCurrency += ".00"
    return commaSeparatedCurrency