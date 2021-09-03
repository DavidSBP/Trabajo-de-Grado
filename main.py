#Importe de librerias.
import random

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
from tensorflow.python.framework import ops
import json
import pickle

#Funcion nltk.download por si la libreria no se importa de manera correcta.
#nltk.download('punkt')

with open("nota.json", encoding = 'utf-8') as file:
    data = json.load(file)

#Seccion para crear o importar las variables principales usadas por el programa.
try:
    with open("variables.pickle","rb") as archivoPickle:
        palabras, tags, entrenamiento, salida = pickle.load(archivoPickle)
except:
    palabras=[]
    tags=[]
    auxX=[]
    auxY=[]

    for contenido in data["contenido"]:
        for patrones in contenido["patrones"]:
            auxPalabra= nltk.word_tokenize(patrones)
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(contenido["tag"])

        if contenido["tag"] not in tags:
            tags.append(contenido["tag"])

    palabras = [stemmer.stem(w.lower()) for w in palabras if w!="?"]
    palabras = sorted(list(set(palabras)))
    tags = sorted(tags)

    entrenamiento = []
    salida = []

    salidaVacia=[0 for _ in range(len(tags))]

    for x, documento in enumerate(auxX):
        cubeta=[]
        auxPalabra=[stemmer.stem(w.lower()) for w in documento]
        for w in palabras:
            if w in auxPalabra:
                cubeta.append(1)
            else:
                cubeta.append(0)
        filaSalida= salidaVacia[:]
        filaSalida[tags.index(auxY[x])]=1
        entrenamiento.append(cubeta)
        salida.append(filaSalida)

    entrenamiento = numpy.array(entrenamiento)
    salida = numpy.array(salida)
    with open("variables.pickle","wb") as archivoPickle:
        pickle.dump((palabras,tags,entrenamiento,salida),archivoPickle)

#seccion para crear la red neuronal.
ops.reset_default_graph()

red = tflearn.input_data(shape=[None,len(entrenamiento[0])])
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, len(salida[0]),activation="softmax")
red = tflearn.regression(red)

#seccion para crear o cargar el Modelo tflearn.
try:
    modelo = tflearn.DNN(red)
    modelo.load("modelo.tflearn")
except:
    modelo = tflearn.DNN(red)
    modelo.fit(entrenamiento,salida,n_epoch=1000,batch_size=10, show_metric=True)
    modelo.save("modelo.tflearn")


#funcion proncipal para el funcionamiento del bot
def mainbot():
    while True:
        entrada = input("Tu: ")
        cubeta=  [0 for _ in range(len(palabras))]
        entradaProcesada = nltk.word_tokenize(entrada)
        entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
        for palabraIndividual in entradaProcesada:
            for i, palabra in enumerate(palabras):
                if palabra == palabraIndividual:
                    cubeta[i] = 1
        resultados = modelo.predict([numpy.array(cubeta)])
        resultadosIndices = numpy.argmax(resultados)
        tag=tags[resultadosIndices]

        for tagAux in data["contenido"]:
            if tagAux["tag"]==tag:
                respuesta = tagAux["respuesta"]
        print("Bot: ",random.choice(respuesta))

mainbot()