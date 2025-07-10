import pickle as pk
import pandas as pd
import json
import os


path__ = os.getcwd()
if "/app" == path__:
    PATH = path__+"/"
else:
    PATH = path__.split('Billettkontroll-AI')[0] + 'Billettkontroll-AI/'

def get_linje_cat():
    return pk.load(open(PATH + 'categories/linjeCat.pkl', 'rb'))


def get_fra_cat():
    return pk.load(open(PATH + 'categories/fraCat.pkl', 'rb'))


def get_til_cat():
    return pk.load(open(PATH + 'categories/tilCat.pkl', 'rb'))


def get_fullt_cat():
    return pk.load(open(PATH + 'categories/fulltCat.pkl', 'rb'))


def get_sjekket_cat():
    return pk.load(open(PATH + 'categories/sjekketCat.pkl', 'rb'))


# Formatting and returning categories
def getLinjer():
    """
    Converts "linjer" Categorical to list and formats to frontend.
    """
    linjeCat = get_linje_cat()
    linjer = list(linjeCat.categories)
    linjer = [l.upper() for l in linjer]
     
    return linjer   
    #return render_template('index.html', linje_list=linjer)


def getFra():
    """
    Converts "fra" Categorical to list and formats to frontend.
    """
    fraCat = get_fra_cat()
    fraList = list(fraCat.categories)
    fraList = [f.replace("_", " ") for f in fraList]
    fraList = [f.capitalize() for f in fraList]
    return fraList


def getTil():
    """
    Converts "til" Categorical to list and formats to frontend.
    """
    tilCat = get_til_cat()
    tilList = list(tilCat.categories)
    tilList = [t.replace("_", " ") for t in tilList]
    tilList = [t.capitalize() for t in tilList]
    return tilList


def getFullt():
    """
    Converts "fullt" Categorical to list and formats to frontend.
    """
    fulltCat = get_fullt_cat()
    fulltList = list(fulltCat.categories)
    fulltList = [f.replace("_", " ") for f in fulltList]
    fulltList = [f.capitalize() for f in fulltList]
    return fulltList


def getCats():
    """
    Gets all the categories in lists and formatted.

    Returns:
        linjer: Linjer in list
        fraList: Fra in list
        tilList: Til in list
        fulltList: Fullt in list
    """
    
    linjer = getLinjer()
    fraList = getFra()
    tilList = getTil()
    fulltList = getFullt()

    return linjer, fraList, tilList, fulltList


def get_cat_with_name(name: str):
    match name:
        case "linje":
            return get_linje_cat()
        case "fra":
            return get_fra_cat()
        case "til":
            return get_til_cat()
        case "fullt":
            return get_fullt_cat()
        case _:
            return None


# Finding cat index for string value
def findCatCode(category_list: pd.Categorical, check_value: str) -> int:
    """Finding the correct category int value for string value.

    Args:
        category_list (pd.Categorical): List of all items in category.
        check_value (str): The str value of the desired category index.

    Returns:
        int: int value of str category index.
    """
    
    for i in range(len(category_list)):
        if category_list[i] == check_value:
            code = category_list.codes[i]
            return int(code)
    raise RuntimeError


# Cleans and formats strings for training use
def strCleaner(x: str) -> str:
    """
    Sets all strings to lowercase and replaces blank spaces with "_".
    Checks if the string includes "ja", then set string to "ja".
    """
    x = x.lower()
    x = x.strip()
    x = x.replace(" ", "_")

    if "ja" in x:
        return "ja"

    return x


# Date and time separaters and formatters
def dateSeparater(date: str):
    """
    Separates a date string from JSON-object to month and date in int.

    Args:
        date (str): The date string from JSON

    Returns:
        month: Month in int format
        day: Day in int format
    """
    
    date = date[5:]
    month = int(date[:2])
    day = int(date[3:])
    return month, day


def timeSeparater(time: str):
    """
    Separates hour and minute from clock string and converts to int.

    Args:
        time (str): The inpur clock value in str format.

    Returns:
        hour: Hour in int format.
        minute: Minutes in int format.
    """
    
    hour = int(time[:2])
    minute = int(time[3:])
    
    return hour, minute


# Converting list data to dict data
def create_predict_data(form_values: list) -> dict:
    """Puts all the form data into a dict.

    Args:
        form_values (list): Form values as strings from the frontend form. 

    Returns:
        dict: The data in dict format.
    """
    linjeCat = get_linje_cat()
    fraCat = get_fra_cat()
    tilCat = get_til_cat()
    fulltCat = get_fullt_cat()

    month, day = dateSeparater(form_values[4])
    hour, minute = timeSeparater(form_values[5])
    
    data = {"Linje": [findCatCode(linjeCat, form_values[0])],
        #"Vogn": [findCatCode(vognCat, int_features[1])],
        "Fra": [findCatCode(fraCat, form_values[1])], 
        "Til": [findCatCode(tilCat, form_values[2])], 
        "Fullt?": [findCatCode(fulltCat, form_values[3])],
        "Dag": [day],
        "Måned": [month],
        "Time": [hour],
        "Minutt": [minute]}
    
    return data


# Converting dict data to DataFrame
def datadict_to_DataFrame(data: dict) -> pd.DataFrame:
    """
    Converting data dict to pandas.DataFrame format.

    Args:
        data (dict): Data in dict format.

    Returns:
        pd.DataFrame: Data in pandas.DataFrame format.
    """
    X_test = pk.load(open(PATH + 'categories/X_test.pkl', 'rb'))
    tester = X_test
    tester = tester.drop(X_test.index)
    testdb = pd.DataFrame(data)
    tester = pd.concat([tester, testdb])
    return tester


def load_accuracy():
    best_accuracy = pk.load(open(PATH + 'accuracy/best_accuracy.pkl', 'rb'))
    best_accuracy = f"{best_accuracy * 100 : .2f}"
    return best_accuracy


def get_version() -> str:
    with open(PATH + "/ver.txt", "r") as f:
        version = f.read()
    return version


def get_date_best_model() -> str:
    with open(PATH + "models/dates.json", "r") as f:
        dates = json.load(f)
        dates = dates["best_model"]
        return f'{dates["day"]}.{dates["month"]}.{dates["year"]}'


def clockTofloat(x: str) -> float:
    x = x[:-3]
    x = x.replace(":",".")
    x = float(x)
    return x


def extractHour(x):
    return x.hour


def extractMinute(x):
    return x.minute


def findCatCode(l, x: str) -> int:
    for i in range(len(l)):
        if l[i] == x:
            code = l.codes[i]
            return code


def datetimeToInt(dt) -> int:
    # second = dt.second
    minute = dt.minute*1
    hour = dt.hour*10
    day = dt.day*10000
    month = dt.month*1000000
    year = dt.year*100000000
    
    ret = minute+hour+day+month+year
    return ret


def extractDay(dt):
    return dt.day


def extractMonth(dt):
    return dt.month


def extractYear(dt):
    return dt.year


def convert_linje_to_new(linje_inn):
    match linje_inn:
        case 'l14':
            return 'r14'
        case 'l12':
            return 'r12'
        case 'r11':
            return 're11'
        case 'r10':
            return 're10'
    return linje_inn