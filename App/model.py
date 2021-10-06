﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
"""
import math
from DISClib.DataStructures.arraylist import getElement
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sa
import config as cf
assert cf



def newCatalogA():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'Artists': None,
               'Artworks': None,
               'Mediums':None,
               'ArtistConstituent': None,
               'Nationality': None}

    catalog['Artists'] = lt.newList('ARRAY_LIST', cmpfunction = compareArtistID)
    catalog['Artworks'] = lt.newList('ARRAY_LIST', cmpfunction =  compareObjectID)

    catalog['Mediums'] = mp.newMap(1000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapMediums)

    catalog['ArtistConstituent'] =  mp.newMap(2000,
                                              maptype = "CHAINING",
                                              loadfactor = 4.0)

    catalog['Nationality'] = mp.newMap(1000,
                                       maptype='CHAINING',
                                       loadfactor = 4.0)

    return catalog
# Funciones para agregar informacion al catalogo

def addArtists(catalog, artist):
    # Se adiciona el libro a la lista de libros
    lt.addLast(catalog['Artists'], artist)
    # Se obtienen los autores del libro
    # ID = artist['Constituent ID']


def addArtworks(catalog, artwork):
    # Se adiciona el libro a la lista de libros

    if artwork["Date"] == "":
        artwork["Date"] = "999999"

    obra = {
        'ObjectID':artwork['ObjectID'],
        'ConstituentID':artwork['ConstituentID'],
        'Title':artwork['Title'],
        'Medium':artwork['Medium'],
        'Dimensions':artwork['Dimensions'],
        'CreditLine':artwork['CreditLine'],
        'DateAcquired':artwork['DateAcquired'],
        'Department':artwork['Department'],
        'URL':artwork['URL'],
        'Height (cm)':artwork['Height (cm)'],
        'Length (cm)':artwork['Length (cm)'],
        'Weight (kg)':artwork['Weight (kg)'],
        'Width (cm)':artwork['Width (cm)'],
        'Classification':artwork['Classification'],
        'Depth (cm)':artwork['Depth (cm)'],
        'Diameter (cm)':artwork['Diameter (cm)'],
        'Date':artwork['Date']

    }
    lt.addLast(catalog['Artworks'], obra)
    addMedium(catalog,obra)
    addNationality(catalog, obra)

def addMedium(catalog, obra):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        mediums = catalog['Mediums']
        if (obra['Medium'] != ''):
            pubmedium = obra['Medium']
        else:
            pubmedium = "None"
        existyear = mp.contains(mediums, pubmedium)
        if existyear:
            entry = mp.get(mediums,pubmedium)
            medium = me.getValue(entry)
        else:
            medium = newMedium(pubmedium)
            mp.put(mediums, pubmedium, medium)
        lt.addLast(medium['obras'],obra)
        sa.sort(medium['obras'], cmpdate)
    except Exception:
        return None


def newMedium(pubmedium):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'medio': "", "obras": None}
    entry['medio'] = pubmedium
    entry['obras'] = lt.newList('ARRAY_LIST')
    return entry

def addArtistConstituent(catalog, artist):

    artistas = catalog['ArtistConstituent']    
    arti = mp.put(artistas, artist["ConstituentID"], artist)

def addNationality(catalog, obra):

    nationality = catalog['Nationality']

    artistas = obra["ConstituentID"].strip("[]").replace(" ", "").split(",")

    for i in artistas:
        nat = mp.get(catalog["ArtistConstituent"], i)
        nat = me.getValue(nat)
        nat = nat["Nationality"]

        if nat.lower() in (None, "", "unknown", "nationality unknown"):
            nat = "Unknown"

        existe = mp.contains(nationality, nat)
        if existe:
            nal = mp.get(nationality, nat)
            na = me.getValue(nal)
        else:
            na = lt.newList("ARRAY_LIST")
            mp.put(nationality, nat, na)

        lt.addLast(na, obra)

def funcionReqUno(catalog, medium):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    medio = mp.get(catalog['Mediums'], medium)
    if medio:
        return me.getValue(medio)
    return None

def ReqLab6(catalog, nacionalidad):
    nationalities = catalog["Nationality"]

    try:
        nationality = me.getValue(mp.get(nationalities, nacionalidad))
        return lt.size(nationality)
    except Exception:
        print("No se encotrno ninguna obra de esa nacionalidad")

def cmpFunctionRuno(anouno, anodos):
    return (int(anouno["BeginDate"]) < int(anodos["BeginDate"]))

def cmpobjectid(iduno, iddos):
    return (int(iduno["ObjectID"]) < int(iddos["ObjectID"]))

def cmpFunctionIndice(artist1, artist2):
    return (int(artist1["ConstituentID"]) < int(artist2["ConstituentID"]))

def cmpcount(countuno, countdos):
    return (int(countuno["Count"])> int(countdos["Count"]))

def cmpFunctionRdos(feuno, fedos):
    fechauno= feuno["DateAcquired"]
    fechados = fedos["DateAcquired"]
    if (fechauno!=None) and (fechauno!=""):
        mini= fechauno[0:4]+fechauno[5:7]+fechauno[8:10]
        mini= int(mini)
    else:
        mini=0
    if (fechados!=None) and (fechados!=""):
        maxi= fechados[0:4]+fechados[5:7]+fechados[8:10]
        maxi= int(maxi)
    else:
        maxi=0
    return (int(mini) < int(maxi))


def cmpnationality(nat1, nat2):
    return nat1["Nationality"] < nat2["Nationality"]

def cmpsize(obras1, obras2):
    return int(lt.size(obras1["obras"])) > int(lt.size(obras2["obras"]))

def compareObjectID(artwork1, artwor2):
    if (artwork1["ObjectID"] == artwor2['ObjectID']):
        return 0
    elif (artwork1["ObjectID"] > artwor2['ObjectID']):
        return 1
    return -1

def compareArtistID(artwork1, artwor2):
    if (artwork1["ConstituentID"] == artwor2['ConstituentID']):
        return 0
    elif (artwork1["ConstituentID"] > artwor2['ConstituentID']):
        return 1
    return -1

def cmpIDArtistas(artista1, artista2):
    return int(artista1["ConstituentID"]) < int(artista2["ConstituentID"])

def cmpunique(obra1, obra2):
    return int(obra1["ObjectID"])<int(obra2["ObjectID"])

def cmpdept(deptuno,deptdos):
    return (deptuno["Department"]<deptdos["Department"])

def cmpdate(dateuno, datedos):
    return (int(dateuno['Date'])<int(datedos['Date']))

def cmpcost(costuno, costdos):
    return (float(costuno['TransCost (USD)'])>float(costdos['TransCost (USD)']))

    #===========================================
    #EL COMPARE FUNCTION PARA EL MAP NUEVO
    #===========================================

def compareMapMediums(med, entry):
    """
    Compara DOS MEDIUMS, med es un identificador
    y entry una pareja llave-valor
    """
    medentry = me.getKey(entry)
    if (med == medentry):
        return 0
    elif (med > medentry):
        return 1
    else:
        return -1
