import numpy as np
import pandas as pd
from flask import Flask, request, render_template
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

@app.route('/')
def home():
    return getCats()
    #return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    form_values = [strCleaner(x) for x in request.form.values()]

    data = {"Linje": [findCatCode(linjeCat, form_values[0])], 
          #"Vogn": [findCatCode(vognCat, int_features[1])],
          "Fra": [findCatCode(fraCat, form_values[1])], 
          "Til": [findCatCode(tilCat, form_values[2])], 
         "Fullt?": [findCatCode(fulltCat, form_values[3])],
         "Dag": [form_values[4]],
         "Måned": [form_values[5]],
         "Time": [form_values[6]],
         "Minutt": [form_values[7]]}
    
    X_test = pk.load(open('./categories/X_test.pkl', 'rb'))
    tester = X_test
    tester = tester.drop(X_test.index)
    testdb = pd.DataFrame(data)
    tester = pd.concat([tester, testdb])

    prediction = model.predict(tester)

    ja = findCatCode(sjekketCat, 'ja')
    nei = findCatCode(sjekketCat, 'nei')

    if prediction[0] == ja:
        output = "Ja, det er sannsynlig for å bli kontrollert"
    else:
        output = "Nei, det er liten sannsynlighet for å bli kontrollert"
    
    return render_template('modal.html', modal_text=output)
    #return render_template('index.html', prediction_text=f"The models says: {output}")
    
@app.route('/modal')
def modal():
    return render_template('modal.html', modal_text='Hello World!')
    
# Need to be addressed
# Same with the clock input
@app.route('/date')
def datoTest():
    form = [strCleaner(x) for x in request.form.values()]
    print(form)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8080')