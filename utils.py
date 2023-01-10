import pickle as pk
import pandas as pd

# Importing all category files from training
linjeCat = pk.load(open('./categories/linjeCat.pkl', 'rb'))
vognCat = pk.load(open('./categories/vognCat.pkl', 'rb'))
fraCat = pk.load(open('./categories/fraCat.pkl', 'rb'))
tilCat = pk.load(open('./categories/tilCat.pkl', 'rb'))
fulltCat = pk.load(open('./categories/fulltCat.pkl', 'rb'))
sjekketCat = pk.load(open('./categories/sjekketCat.pkl', 'rb'))

# Formatting and returning categories
def getLinjer():
    """
    Converts linjer Categorical to list and formats to frontend.
    """
    
    linjer = list(linjeCat.categories)
    linjer = [l.upper() for l in linjer]
     
    return linjer   
    #return render_template('index.html', linje_list=linjer)

def getFra():
    """
    Converts fra Categorical to list and formats to frontend.
    """
    
    fraList = list(fraCat.categories)
    fraList = [f.replace("_", " ") for f in fraList]
    fraList = [f.capitalize() for f in fraList]
    
    return fraList

def getTil():
    """
    Converts til Categorical to list and formats to frontend.
    """
    
    tilList = list(tilCat.categories)
    tilList = [t.replace("_", " ") for t in tilList]
    tilList = [t.capitalize() for t in tilList]
    
    return tilList

def getCats():
    """
    Gets all the categories in lists and formatted.

    Returns:
        linjer: Linjer in list
        fraList: Fra in list
        tilList: Til in list
    """
    
    linjer = getLinjer()
    fraList = getFra()
    tilList = getTil()

    return linjer, fraList, tilList


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
    X_test = pk.load(open('./categories/X_test.pkl', 'rb'))
    tester = X_test
    tester = tester.drop(X_test.index)
    testdb = pd.DataFrame(data)
    tester = pd.concat([tester, testdb])
    return tester

def load_accuracy():
    best_accuracy = pk.load(open('./accuracy/best_accuracy.pkl', 'rb'))
    best_accuracy = f"{best_accuracy * 100 : .2f}"
    return best_accuracy