"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from DISClib.Algorithms.Sorting import mergesort as sa
from time import process_time
from prettytable import PrettyTable, ALL
import sys 
default_limit = 1000 
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar obras de un artista por tecnica")
    print("5- Organizar obras por nacionalidad")
    print("6- Transportar obras de un Departamento")
    print("7- SALIR")


def initCatalogA():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalogA()


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)

def ReqUno(catalog, inicial, final):
    ordenado= controller.funcionReqUnoReto(catalog,inicial,final)
    tamanio = lt.size(ordenado)
    print("============= Req No. 1 Inputs =============")
    print("Artist born between " + str(inicial) + " and " + str(final) + "\n")
    print("============= Req No. 1 Answer =============")
    print("There are " + str(tamanio) + " artist born between " + str(inicial) + " and " + str(final) + "\n")
    print("The first and last 3 artists in range are")
    x = PrettyTable()
    x.field_names = (["ConstituentID","DisplayName","BeginDate","Nationality","Gender","ArtistBio","Wiki QID","ULAN"])
    x.max_width = 25
    x.hrules=ALL

    for i in range(1, 4):
        artista = lt.getElement(ordenado, i)
        
        x.add_row([artista["ConstituentID"], artista["DisplayName"], artista["BeginDate"],
                   artista["Nationality"], artista["Gender"], artista["ArtistBio"], 
                   artista["Wiki QID"], artista["ULAN"]])
    for i in range((lt.size(ordenado)-2), lt.size(ordenado)+1):
        artista = lt.getElement(ordenado, i)
        
        x.add_row([artista["ConstituentID"], artista["DisplayName"], artista["BeginDate"],
                   artista["Nationality"], artista["Gender"], artista["ArtistBio"], 
                   artista["Wiki QID"], artista["ULAN"]])
    print(x)

def ReqDos(catalog, inicial, final):
    resultado = controller.ReqDos(catalog, inicial, final)
    data = resultado[0]
    tamanio = lt.size(data)
    purch = resultado[1]
    print("============= Req No. 2 Inputs =============")
    print("Artworks acquired between" + str(inicial) + " and " + str(final) + "\n")
    print("============= Req No. 2 Answer =============")
    print("The MoMA aqcuired " + str(tamanio) + "  unique pieces between " + str(inicial) + " and " + str(final) + "\n")
    print("Purchased " + str(purch) + " of them \n")
    print("The first and last 3 artists in range are")
    x = PrettyTable()
    x.field_names = (["ObjectID","Title","ArtistNames","Medium","Dimensions","Date","DateAcquired","URL"])
    x.max_width = 25
    x.hrules=ALL

    for i in range(1, 4):
        obra = lt.getElement(data, i)
        
        x.add_row([obra["ObjectID"], obra["Title"], obra["ConstituentID"],
                   obra["Medium"], obra["Dimensions"], obra["Date"], 
                   obra["DateAcquired"], obra["URL"]])
    for i in range((lt.size(data)-2), lt.size(data)+1):
        obra = lt.getElement(data, i)
        
        x.add_row([obra["ObjectID"], obra["Title"], obra["ConstituentID"],
                   obra["Medium"], obra["Dimensions"], obra["Date"], 
                   obra["DateAcquired"], obra["URL"]])
    print(x)

def funcionReqTres(catalog, nombre):
    tad_medios,tad_obras,contador = controller.funcionReqTres(catalog, nombre)
    if tad_medios=="NOHAYOBRAS":
        print("THERE ARE NO WORKS BY THAT AUTHOR")
    elif tad_medios=="NOHAYAUTOR":
        print("THE AUTHOR IS NOT REGISTERED IN THE DATA BASE")
    else:
        size = lt.size(tad_medios)
        sizes = mp.size(tad_obras)
        primer = lt.getElement(tad_medios,1)
        coso = mp.get(tad_obras, primer['Medium'])
        coso = me.getValue(coso)
        paraid = lt.getElement(coso, 1)
        const = paraid["ConstituentID"]
        print("============= Req No. 3 Inputs =============")
        print("Examine the work of the artist named: " + str(nombre) + "\n")
        print("============= Req No. 3 Answer =============")
        print(str(nombre)+ " with MoMA ID " + str(const) + " has " + str(contador) + "pieces in hisher name at the museum \n")
        print("There are "+ str(size) +"different mediums in his her work")
        print("Her his top 5 techniques are:")
        x = PrettyTable()  
        x.field_names = (["Medium","Count"])
        x.max_width = 25
        x.hrules=ALL
        if size >= 5:
            for i in range(1, 6):
                medio = lt.getElement(tad_medios, i)
                x.add_row([medio["Medium"], medio["Cant"]])
    
        else:
            for i in range(1,size+1):
                medio = lt.getElement(tad_medios, i)
                x.add_row([medio["Medium"], medio["Cant"]])
        print(x)
        lamas = lt.getElement(tad_medios,1)
        usada = lamas['Medium']
        numero = lamas['Cant']
        print("His her most used medium is: " + str(usada) + " with "+ str(numero)+"pieces")
        y = PrettyTable()
        y.field_names = (["ObjectID","Title", "Medium", "Dimensions",
                      "DateAcquired", "Classification", "URL"])
        y.max_width = 25
        y.hrules=ALL
        if lt.size(coso) >= 3:
            for i in range(1, 4):
                artwork = lt.getElement(coso, i)
            
                y.add_row([artwork["ObjectID"], artwork["Title"], 
                        artwork["Medium"], artwork["Dimensions"], artwork["DateAcquired"],artwork["Classification"], 
                        artwork["URL"]])
        else:
            for i in range(1,lt.size(coso)+1):
                artwork = lt.getElement(coso, i)
                y.add_row([artwork["ObjectID"], artwork["Title"], 
                        artwork["Medium"], artwork["Dimensions"], artwork["DateAcquired"],artwork["Classification"], 
                        artwork["URL"]])
        print(y)


def ReqCuatro(catalog):
    data = controller.ReqCuatro(catalog)

    print("============= Req No. 4 Inputs =============")
    print("Ranking countries by their number of artworks in the MoMA... \n")
    print("============= Req No. 4 Answer =============")
    print("The TOP 10 countries in the MoMA are:")
    
    x = PrettyTable()
    x.field_names = (["Nationality", "ArtWorks"])
    x.hrules= ALL

    for i in range(1, 11):
        ele = lt.getElement(data, i)
        x.add_row([ele["Nationality"], ele["size"]])

    print(x)

    top = lt.getElement(data, 1)

    print("The TOP nationality in the museum is: " + str(top["Nationality"]) + " with " + str(top["size"]) + " pieces")
    x = PrettyTable()
    x.field_names = (["ObjectID","Title","ArtistNames","Medium","Date","Dimensions","Department", "Classification", "URL"])
    x.max_width = 25
    x.hrules=ALL

    for i in range(1, 4):
        obra = lt.getElement(top["Artworks"], i)
        
        x.add_row([obra["ObjectID"], obra["Title"], obra["ConstituentID"],
                   obra["Medium"], obra["Date"], obra["Dimensions"], 
                   obra["Department"], obra["Classification"], obra["URL"]])
    for i in range((lt.size(top["Artworks"])-2), lt.size(top["Artworks"])+1):
        obra = lt.getElement(top["Artworks"], i)
        
        x.add_row([obra["ObjectID"], obra["Title"], obra["ConstituentID"],
                   obra["Medium"], obra["Date"], obra["Dimensions"], 
                   obra["Department"], obra["Classification"], obra["URL"]])
    print(x)

def funcionReqCin(catalog, nombre):
    costo,tad_antiguas,tad_costosas, pesototal = controller.funcionReqCin(catalog, nombre)
    if lt.size(tad_antiguas)==0:
        print("THERE ARE NO WORKS BY THAT DEPARTMENT")
    else:
        size = lt.size(tad_costosas)
        sizes = lt.size(tad_antiguas)
        print("============= Req No. 5 Inputs =============")
        print("Estimate the cost to transport all artifacts in " + str(nombre) + "MoMA's Department\n")
        print("============= Req No. 5 Answer =============")
        print("The MoMA is going to transport " + str(sizes) +"artifacts from: "+str(nombre) +" \n")
        print("REMEMBER!! NOT all MoMA's data is complete!!!...These are estimates")
        print("Estimated Cargo Weight:"+str(pesototal))
        print("Estimated cargo cost:"+str(costo))
        print("The TOP 5 most expensive items to transport are: ")
        x = PrettyTable()  
        x.field_names = (["ObjectID","Title", "ArtistsNames", "Medium", "Date", "Dimensions", "Classification", "TransCost (USD)", "URL"])
        x.max_width = 25
        x.hrules=ALL
        if size >= 5:
            for i in range(1, 6):
                artwork = lt.getElement(tad_costosas, i)
                x.add_row([artwork["ObjectID"], artwork["Title"], artwork['Artists'], 
                        artwork["Medium"], artwork['Date'], artwork["Dimensions"],artwork["Classification"], 
                        artwork['TransCost (USD)'], artwork["URL"]])
    
        else:
            for i in range(1,size+1):
                artwork = lt.getElement(tad_costosas, i)
                x.add_row([artwork["ObjectID"], artwork["Title"], artwork['Artists'], 
                        artwork["Medium"], artwork['Date'], artwork["Dimensions"],artwork["Classification"], 
                        artwork['TransCost (USD)'], artwork["URL"]])
        print(x)
        print("The TOP 5 oldest items to transport are: ")
        y = PrettyTable()  
        y.field_names = (["ObjectID","Title", "ArtistsNames", "Medium", "Date", "Dimensions", "Classification", "TransCost (USD)", "URL"])
        y.max_width = 25
        y.hrules=ALL
        if size >= 5:
            for i in range(1, 6):
                artwork = lt.getElement(tad_antiguas, i)
                y.add_row([artwork["ObjectID"], artwork["Title"], artwork['Artists'], 
                        artwork["Medium"], artwork['Date'], artwork["Dimensions"],artwork["Classification"], 
                        artwork['TransCost (USD)'], artwork["URL"]])
    
        else:
            for i in range(1,size+1):
                artwork = lt.getElement(tad_antiguas, i)
                y.add_row([artwork["ObjectID"], artwork["Title"], artwork['Artists'], 
                        artwork["Medium"], artwork['Date'], artwork["Dimensions"],artwork["Classification"], 
                        artwork['TransCost (USD)'], artwork["URL"]])
        print(y)

#def ReqLab6(catalog, nacionalidad):
    #size = controller.ReqLab6(catalog, nacionalidad)
    #print("============= Req Lab. 6 Inputs =============")
    #print("Artworks of the nationality " + nacionalidad + "\n")
    #print("============= Req Lab. 6 Answer =============")
    #print("There are " + str(size) + " artworks of the nationality " + nacionalidad  + "\n")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initCatalogA()
        t1 = process_time()
        loadData(catalog)
        t2 = process_time()
        print("Cargando información de los archivos ....\n")
        #Nationality
        print('Artistas cargados: ' + str(mp.size(catalog["ArtistConstituent"])) + "\n")
        print('Obras cargadas: ' + str(catalog['Artworks'])+"\n")
        print('Dpst cargados: ' + str(mp.size(catalog['Depts']))+"\n")
        #print('Nacionalidades cargadas: ' + str(mp.size(catalog['Nationality']))+"\n")
        print("Time = " + str(t2 - t1) + "seg \n")
        
    elif int(inputs[0]) == 2:
        inicial = input("Ingrese el año inicial: \n")
        final = input("Ingrese el año final: \n")
        t1 = process_time()
        ReqUno(catalog, inicial, final)
        t2 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")

    elif int(inputs[0]) == 3:
        inicial = input("Ingrese el año inicial (AAAA-MM-DD): \n")
        final = input("Ingrese el año final (AAAA-MM-DD): \n")
        t1 = process_time()
        ReqDos(catalog, inicial, final)
        t2 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")

    elif int(inputs[0]) == 4:
        elnombre = input("Ingrese el nombre del artista: \n")
        t1 = process_time()
        funcionReqTres(catalog, elnombre)
        t2 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")

    elif int(inputs[0]) == 5:
        t1 = process_time()
        ReqCuatro(catalog)
        t2 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")
    elif int(inputs[0]) == 6:
        elnombre = input("Ingrese el nombre del dept: \n")
        t1 = process_time()
        funcionReqCin(catalog, elnombre)
        t2 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")
    else:
        sys.exit(0)
sys.exit(0)