import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
import pickle as pk


def findCatCode(l, x: str):
    for i in range(len(l)):
        if l[i] == x:
            code = l.codes[i]
            return code

def strCleaner(x: str) -> str:
    x = x.lower()
    x = x.replace(" ", "_")

    if "ja" in x:
        return "ja"

    return x

linjeCat = pk.load(open('./categories/linjeCat.pkl', 'rb'))
vognCat = pk.load(open('./categories/vognCat.pkl', 'rb'))
fraCat = pk.load(open('./categories/fraCat.pkl', 'rb'))
tilCat = pk.load(open('./categories/tilCat.pkl', 'rb'))
fulltCat = pk.load(open('./categories/fulltCat.pkl', 'rb'))
sjekketCat = pk.load(open('./categories/sjekketCat.pkl', 'rb'))

app = Flask(__name__)

model = pk.load(open('./models/model.pkl', 'rb'))

# Gets the categorical data form the model testing
def getLinjer():
    linjer = list(linjeCat.categories)
    linjer = [l.upper() for l in linjer]
     
    return linjer   
    #return render_template('index.html', linje_list=linjer)


def getFra():
    fraList = list(fraCat.categories)
    fraList = [f.replace("_", " ") for f in fraList]
    fraList = [f.capitalize() for f in fraList]
    
    return fraList

def getTil():
    tilList = list(tilCat.categories)
    tilList = [t.replace("_", " ") for t in tilList]
    tilList = [t.capitalize() for t in tilList]
    
    return tilList

def getCats():
    """Gets all the categories from the cat-files and return a render_template

    Returns:
        render_template with all variables for lists
    """
    
    linjer = getLinjer()
    fraList = getFra()
    tilList = getTil()
    
    return render_template('index.html', linje_list=linjer, fra_list=fraList, til_list=tilList)

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
    hour = int(time[:2])
    minute = int(time[3:])
    
    return hour, minute

@app.route('/')
def home():
    return getCats()
    #return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    form_values = [strCleaner(x) for x in request.form.values()]

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
    
    if app.debug:
        print(data)
    
    X_test = pk.load(open('./categories/X_test.pkl', 'rb'))
    tester = X_test
    tester = tester.drop(X_test.index)
    testdb = pd.DataFrame(data)
    tester = pd.concat([tester, testdb])

    prediction = model.predict(tester)

    ja = findCatCode(sjekketCat, 'ja')
    #nei = findCatCode(sjekketCat, 'nei')

    if prediction[0] == ja:
        output = "Ja, det er sannsynlig for å bli kontrollert"
    else:
        output = "Nei, det er liten sannsynlighet for å bli kontrollert"
    
    return render_template('modal.html', modal_text=output)
    #return render_template('index.html', prediction_text=f"The models says: {output}")
    
    
    
    
# TESTING
@app.route('/modal')
def modal():
    return render_template('modal.html', modal_text='Hello World!')
    
@app.route('/date', methods=['POST'])
def datoTest():
    date = request.form.get('date')
    # Removes year
    date = date[5:]
    
    month = int(date[:2])
    day = int(date[3:])
    print(f"Date: {date}\nMonth: {month}\nDay: {day}")
    return redirect(url_for('home'))

@app.route('/time', methods=['POST'])
def timeTest():
    time = request.form.get('time')
    print(time)
    
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8080')