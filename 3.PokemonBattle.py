from flask import Flask, abort, render_template, request, send_from_directory, url_for, redirect,jsonify
import requests
import json
import joblib
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        poke1= request.form['pokemon1']
        poke2= request.form['pokemon2']
        poki1 = poke1.lower()
        poki2 = poke2.lower()
        url_poke1 = 'https://pokeapi.co/api/v2/pokemon/'+poki1
        url_poke2 = 'https://pokeapi.co/api/v2/pokemon/'+poki2
        raw_data1 = requests.get(url_poke1)
        raw_data2 = requests.get(url_poke2)
        if str(raw_data1) == '<Response [404]>' or str(raw_data2) == '<Response [404]>':
            return render_template('notFound.html')
        else:    
            data1 = raw_data1.json()
            data2 = raw_data2.json()
            nama_pokemon1 = data1['forms'][0]['name']
            nama_pokemon2 = data2['forms'][0]['name']           
            url_image1 = data1['sprites']['front_default']
            url_image2 = data2['sprites']['front_default']
             
            data1 = pokemon[pokemon['Name'] == nama_pokemon1.capitalize()][['HP','Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.tolist()
            data2 = pokemon[pokemon['Name'] == nama_pokemon2.capitalize()][['HP','Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.tolist()
            if len(data1) == 0 or len(data2)== 0:
                return render_template('notFound.html')
            else:                      
                img = io.BytesIO()
                Label = ['HP', 'Attack', 'Defense', 'Sp Attack', 'Sp Defense', 'Speed', ]
                
                x = np.arange(len(Label))
                width = 0.3
                plt.bar(x - width/2, data1[0], width, label=nama_pokemon1.capitalize(), color='pink')
                plt.bar(x + width/2, data2[0], width, label=nama_pokemon2.capitalize(), color='#00688b')
                plt.xticks(ticks=x, labels=Label)
                plt.legend()
                plt.tight_layout()
                plt.savefig(img, format='png', transparent=True)
                plt.close()
                img.seek(0)

                plot_url = base64.b64encode(img.getvalue()).decode()

                input_data = data1[0]
                input_data.extend(data2[0])
                prediksi = model.predict([input_data])[0]
                print(prediksi)
                if prediksi == 0:
                    winner = nama_pokemon2.upper()
                    probabilitas = round(model.predict_proba([input_data])[0][0]*100, 2)
                else:
                    winner = nama_pokemon1.upper()
                    probabilitas = round(model.predict_proba([input_data])[0][1]*100, 2)
                print(probabilitas)
                hasil = {
                'nama_pokemon1' : nama_pokemon1.upper(), 'nama_pokemon2' : nama_pokemon2.upper(),
                'url_image1' : url_image1, 'url_image2' : url_image2,
                'winner' : winner, 'probabilitas' : probabilitas
                }
                print(winner)
                
                return render_template('result.html', hasil=hasil, plot_url=plot_url )

    else:
        return redirect(url_for('home'))
#========================================================================================================
# TEMP IMAGE
@app.route('/filetemp/<path:path>')                           
def filetemp(path):
    return send_from_directory('./templates/image', path)

@app.errorhandler(404)                                              
def notFound(error) :                                               
    return render_template('error.html')

if __name__ == '__main__':
    pokemon, model = joblib.load('modelpokemon')                 
    app.run(debug = True)  