import json

def numtag(numero,tam):
    numstr = str(numero)
    cadena=""
    if len(numstr)<tam:
        for i in range(tam-len(numstr)):
            cadena+="0"
        cadena+=numstr
    else:
        cadena=numstr
    return cadena

def importar(ruta_archivo):
    archivo = open(ruta_archivo,"r")
    base = {"contenido": []}
    for i in range(556):
        dic={}
        linea = archivo.readline()
        dic["tag"] = numtag(i,4)
        dic["patrones"] = linea
        dic["respuesta"] = linea
        base["contenido"].append(dic)

    archivo.close()

    with open("base.json", "w") as archivo:
        json.dump(base,archivo)
        print("archivo creado")