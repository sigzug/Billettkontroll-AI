import logging
import os

from flask import Flask, Response, request, render_template, redirect, url_for

from training.utils.utils import *


DEBUG_MODE = False

logging.basicConfig(level=logging.DEBUG,
                    filename='./logs/deploy.log',
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s') 

app = Flask(__name__)

model = pk.load(open('models/best_model.pkl', 'rb'))


@app.route('/')
def home():
    linjer, fraList, tilList, fulltList = getCats()
    best_accuracy = load_accuracy()
    version = get_version()
    date = get_date_best_model()

    return render_template('index.html', linje_list=linjer, fra_list=fraList, til_list=tilList, fullt_list=fulltList, best_accuracy=best_accuracy, version=version, date=date)
    #return render_template('index.html')
    

@app.route('/predict', methods=['POST'])
def predict():

    form_values = [strCleaner(x) for x in request.form.values()]
    
    # Putting data into dict
    data = create_predict_data(form_values)
    
    if DEBUG_MODE:
        print(f"Data: \n{data}\n")
    
    # Converting dict to pandas DataFrame in trining data format
    tester = datadict_to_DataFrame(data)

    prediction = model.predict(tester)

    sjekketCat = get_sjekket_cat()
    ja = findCatCode(sjekketCat, 'ja')
    #nei = findCatCode(sjekketCat, 'nei')

    if prediction[0] == ja:
        output = "Ja, det er sannsynlig for å bli kontrollert"
    else:
        output = "Nei, det er liten sannsynlighet for å bli kontrollert"
    
    return render_template('modal.html', modal_text=output)
    #return render_template('index.html', prediction_text=f"The models says: {output}")
   
    

######## TESTING ########
@app.route('/modal')
def modal():
    if DEBUG_MODE:
        logging.debug("Loaded /modal successfully.")
        return render_template('modal.html', modal_text='Hello World!')
    else:
        logging.error("Unauthorized access")
        return Response("Unauthorized!", status=405, mimetype='application/json')
    
@app.route('/date', methods=['POST'])
def datoTest():
    if DEBUG_MODE:
        date = str(request.form.get('date'))
        
        # Removes the year from str
        date = date[5:]

        month = int(date[:2])
        day = int(date[3:])
        print(f"Date: {date}\nMonth: {month}\nDay: {day}")
        return redirect(url_for('home'))
    else:
        logging.error("Unauthorized access")
        return Response("Unauthorized!", status=405, mimetype='application/json')

@app.route('/time', methods=['POST'])
def timeTest():
    if DEBUG_MODE:
        time = request.form.get('time')
        print(time)
        
        return redirect(url_for('home'))
    else:
        logging.error("Unauthorized access")
        return Response("Unauthorized!", status=405, mimetype='application/json')
    
###################

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=8080)
    