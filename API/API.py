from flask import Flask, request, jsonify
import json
from joblib import dump, load
import traceback
import pandas as pd
import numpy as np
import codecs as codecs
import re

app = Flask(__name__)


with codecs.open('positive_words_es.txt','r',encoding='utf8') as f:
    positive_words= f.read()
    
positive_words=positive_words.split('\r\n')

with codecs.open('negative_words_es.txt','r',encoding='utf8') as f:
    negative_words= f.read()
    
negative_words=negative_words.split('\r\n')



# % Mayusculas
def mayusculas(str):
    numMayus = sum(1 for c in str if c.isupper())
    return numMayus/sum(1 for c in str)

# total de signos de interrogación
def numInterrogacionTot(str):
    count = 0
    for i in range (0, len (str)):   
    #Checks whether given character is a punctuation mark  
        if str[i] in ("¿","?"):  
            count = count + 1
    return count

# porcentaje signos de interrogacion        
def numInterrogacionRel(str):
    count = 0
    for i in range (0, len (str)):   
    #Checks whether given character is a punctuation mark  
        if str[i] in ("¿","?"):  
            count = count + 1
    return count/sum(1 for c in str)

# total de signos de exclamacion
def numExclamacionTot(str):
    count = 0
    for i in range (0, len (str)):   
    #Checks whether given character is a punctuation mark  
        if str[i] in ("¡","!"):  
            count = count + 1
    return count

# porcentaje signos de exclamacion        
def numExclamacionRel(str):
    count = 0
    for i in range (0, len (str)):   
    #Checks whether given character is a punctuation mark  
        if str[i] in ("¡","!"):  
            count = count + 1
    return count/sum(1 for c in str)

# palabras positivas
def positiveTot(str): 
    # break the string into list of words 
    str = str.split()
    # loop till string values present in list str 
    count = 0
    for i in range (0, len (str)):
        if str[i] in positive_words:
            count = count + 1;
    return count

def positiveRel(str): 
    # break the string into list of words 
    str = str.split()
    # loop till string values present in list str 
    count = 0
    for i in range (0, len (str)):
        if str[i] in positive_words:  
                count = count + 1;
            
            
    return count/len(str)

# palabras negativas
def negativeTot(str): 
    # break the string into list of words 
    str = str.split()
    # loop till string values present in list str 
    count = 0
    for i in range (0, len (str)):
        if str[i] in negative_words:
            count = count + 1;
    return count

def negativeRel(str): 
    # break the string into list of words 
    str = str.split()
    # loop till string values present in list str 
    count = 0
    for i in range (0, len (str)):
        if str[i] in negative_words:  
                count = count + 1
    return count/len(str)
# palabras unicas / palabras totales
def redundancia(str): 
    # break the string into list of words 
    str = str.split()
    str2 = [] 
    # loop till string values present in list str 
    for i in range (0, len (str)): 
        # checking for the duplicacy 
        if str[i] not in str2: 
            # insert value in str2 
            str2.append(str[i])
 
    rta = len(str2)/len(str) 
            
    return rta
#Contar *NUMBER*
def num(str): 
    # break the string into list of words 
    str = str.split()
    str2 = [] 
    # loop till string values present in list str 
    for i in str: 
        # checking for the duplicacy 
        if i not in str2: 
            # insert value in str2 
            str2.append(i)
    num = 0
    for i in range(0, len(str2)):
        if str2[i] == "*NUMBER*":
            num = str.count(str2[i])
        else:
            continue
            
    return num

def numRel(str): 
    # break the string into list of words 
    str = str.split()
    str2 = [] 
    # loop till string values present in list str 
    for i in str: 
        # checking for the duplicacy 
        if i not in str2: 
            # insert value in str2 
            str2.append(i)
    num = 0
    for i in range(0, len(str2)):
        if str2[i] == "*NUMBER*":
            num = str.count(str2[i])
        else:
            continue
            
    return num/len(str)
def numResults(str):
    if(str=="No results"):
        return 0
    else:
        # Quitar "Cerca de"
        str = str.replace("Cerca de", "")
        # Obtener el número
        str = str.split()
        num= str[0]
        num = num.replace(",", "")
        return int(num)

# total de comillas
def numComillasTot(str):
    count = 0
    for i in range (0, len (str)):   
    #Checks whether given character is a punctuation mark  
        if str[i] in ("«","»","“","”","‘","’","'","\""):  
            count = count + 1
    return count

# porcentaje comillas        
def numComillasRel(str):
    count = 0
    for i in range (0, len (str)):   
    #Checks whether given character is a punctuation mark  
        if str[i] in ("«","»","“","”","‘","’","'","\""):  
            count = count + 1
    return count/sum(1 for c in str)

def replaceNumbers(str):
    return re.sub('[0-9]+','*NUMBER*',str)
      


@app.route('/predict', methods=['POST'])
def predict():
    if rf:
        try:
            json_ = request.json
            headline =replaceNumbers(json_["headline"])
            link =  json_["link"]
            text =  replaceNumbers(json_["text"])

            pMayusculasHeadLine = mayusculas(headline)
            SignosInterrogacion = numInterrogacionTot(text)
            pSignosInterrogacion = numInterrogacionRel(text)
            SignosExclamacion = numExclamacionTot(text)
            pSignosExclamacion = numExclamacionRel(text)
            PalabrasPositivas = positiveTot(text)
            pPalabrasPositivas = positiveRel(text)
            PalabrasNegativas =  negativeTot(text)
            pPalabrasNegativas =  negativeRel(text)
            red =  redundancia(text)
            Numeros =  num(text)
            pNumeros =  numRel(text)
            Comillas =  numComillasTot(text)
            pComillas =  numComillasRel(text)
            ResultadosGoogle = 0 
            ResultadosGoogleNews = 0
            ceroResultadosGoogleNews = 1 if ResultadosGoogleNews==0 else 0
            print(text)
            dictEntrada = {
                '%MayusculasHeadLine': pMayusculasHeadLine,
                '#SignosInterrogación': SignosInterrogacion,
                '%SignosInterrogación': pSignosInterrogacion,
                '#SignosExclamación': SignosExclamacion,
                '%SignosExclamación': pSignosExclamacion, 
                '#PalabrasPositivas': PalabrasPositivas,
                '%PalabrasPositivas': pPalabrasPositivas,
                '#PalabrasNegativas': PalabrasNegativas,
                '%PalabrasNegativas': pPalabrasNegativas,
                'Palabras unicas/palabras totales': red,
                '#Numeros': Numeros,
                '%Numeros': pNumeros,
                '#Comillas': Comillas,
                '%Comillas': pComillas,
                '#ResultadosGoogle': ResultadosGoogle,
                '#ResultadosGoogleNews': ResultadosGoogleNews,
                '0ResultadosGoogleNews': ceroResultadosGoogleNews
            }

            print(dictEntrada)

            #jsonEntrada = json.loads(dictEntrada)
            
            query = pd.DataFrame(dictEntrada, index=[0])
            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(rf.predict(query))
            
            return jsonify({'prediction': str(prediction)})
        except Exception as e:
            print(e)
            return 'holis'
            #return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')


if __name__ == '__main__':
    
    rf = load("model_sinSpanishCorrector.pkl") # Load "model.pkl"
    print ('Model loaded')
    model_columns = load("model_columns.pkl") # Load "model_columns.pkl"
    print ('Model columns loaded')

    app.run(debug=True)