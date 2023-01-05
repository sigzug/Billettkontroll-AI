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

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    int_features = [strCleaner(x) for x in request.form.values()]

    data = {"Linje": [findCatCode(linjeCat, int_features[0])], 
          #"Vogn": [findCatCode(vognCat, int_features[1])],
          "Fra": [findCatCode(fraCat, int_features[1])], 
          "Til": [findCatCode(tilCat, int_features[2])], 
         "Fullt?": [findCatCode(fulltCat, int_features[3])],
         "Dag": [int_features[4]],
         "Måned": [int_features[5]],
         "Time": [int_features[6]],
         "Minutt": [int_features[7]]}
    
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

    return render_template('index.html', prediction_text=f"The models says: {output}")


@app.route('/linje', methods=['GET'])
def getLinje():
    linjeCat = pk.load(open("./categories/linjeCat.pkl", 'rb'))
    linjer = list(linjeCat.categories)
    return render_template('index.html', linje_list=linjer)
    
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8080')