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
    print("2- Las N obras mas antiguas del medio")
    print("3- Numero de obras de una nacionalidad")
    print("4- Listar cronológicamente los artistas")
    print("5- SALIR")


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

def funcionReqLabFive(catalog, medium,eln):
    ordenad= controller.funcionReqUno(catalog,medium)
    ordenado = ordenad["obras"]
    el_n= int(eln)
    tamanio = lt.size(ordenado)
    print("============= Req Lab. 5 Inputs =============")
    print("Artworks of the medium " + str(medium) + "\n")
    print("============= Req Lab. 5 Answer =============")
    print("There are " + str(tamanio) + " artworks of the medium " + str(medium)  + "\n")
    print("The n works are")
    if ordenado==None:
        print("No hay info")
    elif tamanio<el_n:
        x = PrettyTable()
        x.field_names = (["ObjectID","Title", "Medium", "Dimensions","Date",
                      "DateAcquired", "URL"])
        x.max_width = 25
        x.hrules=ALL

        for i in range(0, tamanio+1):
            artwork = lt.getElement(ordenado, i)
            
            x.add_row([artwork["ObjectID"], artwork["Title"],
                    artwork["Medium"], artwork["Dimensions"],artwork["Date"], artwork["DateAcquired"], 
                    artwork["URL"]])
        print(x)

    else:
        x = PrettyTable()
        x.field_names = (["ObjectID","Title", "Medium", "Dimensions","Date",
                      "DateAcquired", "URL"])
        x.max_width = 25
        x.hrules=ALL

        for i in range(1, el_n):
            artwork = lt.getElement(ordenado, i)
            
            x.add_row([artwork["ObjectID"], artwork["Title"], 
                    artwork["Medium"], artwork["Dimensions"], artwork["Date"],artwork["DateAcquired"], 
                    artwork["URL"]])

        print(x)

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


def ReqLab6(catalog, nacionalidad):
    size = controller.ReqLab6(catalog, nacionalidad)
    print("============= Req Lab. 6 Inputs =============")
    print("Artworks of the nationality " + nacionalidad + "\n")
    print("============= Req Lab. 6 Answer =============")
    print("There are " + str(size) + " artworks of the nationality " + nacionalidad  + "\n")


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
        
        print('Artistas cargados: ' + str(lt.size(catalog['Artists'])) + "\n")
        print('Obras cargadas: ' + str(lt.size(catalog['Artworks']))+"\n")
        print("Time = " + str(t2 - t1) + "seg \n")
    
    elif int(inputs[0]) == 2:
        medio=input("Coloque el medio:\n")
        eln=input("Cuantas obras quiere ver:\n")
        t1 = process_time()
        funcionReqLabFive(catalog, medio, eln)
        t2 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")

    elif int(inputs[0]) == 3:
        nacionalidad = input("Ingrese la nacionalidad: \n")
        t1 = process_time()
        size = ReqLab6(catalog, nacionalidad)
        t1 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")
        
    elif int(inputs[0]) == 4:
        inicial = input("Ingrese el año inicial: \n")
        final = input("Ingrese el año final: \n")
        t1 = process_time()
        ReqUno(catalog, inicial, final)
        t1 = process_time()
        print("Time = " + str(t2 - t1) + "seg \n")

    else:
        sys.exit(0)
sys.exit(0)