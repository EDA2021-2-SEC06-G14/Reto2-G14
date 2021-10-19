"""
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
from DISClib.Algorithms.Sorting import mergesort as merge
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

    #catalog['Artists'] = lt.newList('ARRAY_LIST', cmpfunction = compareArtistID)
    catalog['Artworks'] = lt.newList('ARRAY_LIST', cmpfunction =  compareObjectID)

    #catalog['Mediums'] = mp.newMap(100000,
                                   #maptype='PROBING',
                                   #loadfactor=0.5,
                                   #comparefunction=compareMapMediums)

    catalog['ArtistConstituent'] =  mp.newMap(40000,
                                              maptype = "PROBING",
                                              loadfactor = 0.5)
            
    catalog['ArtistConsti'] = mp.newMap(40000,maptype = "PROBING",loadfactor = 0.5)

    catalog['Nationality'] = mp.newMap(1000,
                                       maptype='PROBING',
                                       loadfactor = 0.5)

    catalog['yearsborn'] = mp.newMap(4000,maptype='PROBING',loadfactor = 0.5)
    catalog['Depts'] = mp.newMap(2000,maptype='PROBING',loadfactor = 0.5)

    catalog["DateAcquired"] = mp.newMap(150000, 
                                        maptype= 'PROBING', 
                                        loadfactor = 0.5)



    return catalog
# Funciones para agregar informacion al catalogo

#def addArtists(catalog, artist):
    # Se adiciona el libro a la lista de libros
    #lt.addLast(catalog['Artists'], artist)
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
    addToAuthor(catalog, obra)
    addToDept(catalog,obra)
    addNationality(catalog, obra)
    


def addArtistConstituent(catalog, artist):

    artistas = catalog['ArtistConstituent']    
    arti = mp.put(artistas, artist["ConstituentID"], artist)

def addArtistConsti(catalog, artist):

    artistas = catalog['ArtistConsti'] 
    artist['requetres']= mp.newMap(1000,maptype = "PROBING",loadfactor = 0.5)
    artist['ltrequetres']=lt.newList('ARRAY_LIST')   
    mp.put(artistas, artist["DisplayName"], artist)
    

def addToAuthor(catalog, artwork):
    #requetres = catalog['Nationality']

    artistas = artwork["ConstituentID"].strip("[]").replace(" ", "").split(",")

    for i in artistas:
        nat = mp.get(catalog["ArtistConstituent"], i)
        nat = me.getValue(nat)
        nat = nat["DisplayName"]
        pa_requetres = mp.get(catalog['ArtistConsti'], nat)
        pa_requetres = me.getValue(pa_requetres)
        med_pa_requetres = artwork["Medium"]

        if med_pa_requetres.lower() in (None, "", "unknown"):
            med_pa_requetres = "Unknown"

        existe = mp.contains(pa_requetres['requetres'], med_pa_requetres)
        if existe:
            elmed = mp.get(pa_requetres['requetres'], med_pa_requetres)
            elmedi = me.getValue(elmed)
            lista= pa_requetres['ltrequetres']
            for i in range(1, lt.size(lista)+1):
                ele = lt.getElement(lista, i)
                if ele["Medium"]==med_pa_requetres:
                    ele["Cant"]+=1
        else:
            elmedi = lt.newList("ARRAY_LIST")
            mp.put(pa_requetres['requetres'], med_pa_requetres, elmedi)
            lista= pa_requetres['ltrequetres']
            nuevoele={
                "Medium": med_pa_requetres,
                "Cant":1
            }
            lt.addLast(lista,nuevoele)

        lt.addLast(elmedi,artwork)

def addNationality(catalog, obra):

    nationality = catalog['Nationality']

    artistas = obra["ConstituentID"].strip("[]").replace(" ", "").split(",")

    for i in artistas:
        nat = mp.get(catalog["ArtistConstituent"], i)
        nat = me.getValue(nat)
        nat = nat["Nationality"]

        autores = "-"
        for j in artistas:
            art = mp.get(catalog["ArtistConstituent"], j)
            art = me.getValue(art)["DisplayName"]

            autores = autores + art + "-"

        obra["ConstituentID"] = autores

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

def addArtistBorn(catalog, artist):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        years = catalog['yearsborn']
        if (artist['BeginDate'] != ''):
            bornyear = artist['BeginDate']
            bornyear = int(float(bornyear))
        else:
            bornyear = 99999
        existyear = mp.contains(years, bornyear)
        if existyear:
            entry = mp.get(years, bornyear)
            year = me.getValue(entry)
        else:
            year = newYear(bornyear)
            mp.put(years, bornyear, year)
        lt.addLast(year['artists'], artist)
    except Exception:
        return None


def newYear(bornyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'year': "", "artists": None}
    entry['year'] = bornyear
    entry['artists'] = lt.newList('ARRAY_LIST')
    return entry

def adquisicion(catalog, obra):

    mapa = catalog["DateAcquired"]
    fecha = obra["DateAcquired"][0:4]
    
    if fecha == None:
        fecha = 0

    existe = mp.contains(mapa, fecha)
    if existe:
        list = mp.get(mapa, fecha)
        li = me.getValue(list)
    else:
        li = lt.newList("ARRAY_LIST")
        mp.put(mapa, fecha, li)

    lt.addLast(li, obra)
def addToDept(catalog, obra):
    departamento = obra['Department']
    depts = catalog["Depts"]
    if departamento.lower() in (None, "", "unknown"):
        departamento= "unknown"
    existe = mp.contains(depts,departamento)
    if existe:
        parja= mp.get(depts,departamento)
        listica = me.getValue(parja)
    else:
        listica=lt.newList("ARRAY_LIST")
        mp.put(depts,departamento,listica)
    lt.addLast(listica, obra)

def funcionReqCin(catalog, nombre):
    la_lista=mp.get(catalog["Depts"],nombre)
    la_lista=me.getValue(la_lista)
    cant=lt.size(la_lista)
    costoretotal=0.0
    pesototal=0.0
    cant+=1
    antiguas = lt.newList("ARRAY_LIST")
    costosas = lt.newList("ARRAY_LIST")
    for i in range(1, cant):
        costototal=0.0
        ele = lt.getElement(la_lista,i)
        costopeso=0
        if (ele["Weight (kg)"]==None) or (ele["Weight (kg)"]==''):
            costopeso=float(-1)
        else:
            costopeso = float(ele["Weight (kg)"])*72
            pesototal+= float(ele["Weight (kg)"])
        costomedidas=-1
        if (ele["Height (cm)"]!=None) and (ele["Height (cm)"]!=''):
            if (ele["Width (cm)"]!=None) and (ele["Width (cm)"]!=''):
                if (ele['Depth (cm)']!=None) and (ele['Depth (cm)']!=''):
                    if float(ele['Depth (cm)'])>0:
                        depth= float(ele['Depth (cm)'])/100
                        width = float(ele["Width (cm)"])/100
                        height = float(ele["Height (cm)"])/100
                        m3= depth*width*height
                        costomedidas=m3*72
                    else:
                        width = float(ele["Width (cm)"])/100
                        height = float(ele["Height (cm)"])/100
                        m2= width*height
                        costomedidas=m2*72
                else:
                    width = float(ele["Width (cm)"])/100
                    height = float(ele["Height (cm)"])/100
                    m2= width*height
                    costomedidas=m2*72
            elif (ele["Diameter (cm)"]!=None) and (ele["Diameter (cm)"]!=''):
                radio = float(ele["Diameter (cm)"])/200
                height = float(ele["Height (cm)"])/100
                m3= radio*height*radio*math.pi
                costomedidas=m3*72
        elif (ele["Width (cm)"]!=None) and (ele["Width (cm)"]!=''):
            if (ele['Length (cm)']!=None) and (ele['Length (cm)']!=''):
                width = float(ele["Width (cm)"])/100
                lenght = float(ele["Length (cm)"])/100
                m2=width*lenght
                costomedidas=m2*72
        elif (ele["Diameter (cm)"]!=None) and (ele["Diameter (cm)"]!=''):
            radio = float(ele["Diameter (cm)"])/200
            m2= radio*radio*math.pi
            costomedidas=m2*72
        costototal=max(costopeso,costomedidas)
        if costototal<=0:
            costototal=48.0
        authors = ele["ConstituentID"].strip("[]").replace(" ", "").split(",")
        for x in authors:
            elemento= mp.get(catalog["ArtistConstituent"],x)
            if elemento!=None:
                elemento= me.getValue(elemento)
                autores = autores +"-"+ elemento['DisplayName'] + "-"
        agregar = {
            'ObjectID':ele['ObjectID'],
            'Title':ele['Title'],
            'Artists':ele["ConstituentID"],
            'Medium':ele['Medium'],
            'Dimensions':ele['Dimensions'],
            'DateAcquired':ele['DateAcquired'],
            'Classification':ele['Classification'],
            'TransCost (USD)':str(costototal),
            'URL':ele['URL'],
            'Date':ele['Date']
        }
        lt.addLast(antiguas,agregar)
        lt.addLast(costosas,agregar)
        costoretotal+=costototal
    #AQUI SE SUPONE QUE YA TENEMOS LAS 2 LISTICAS LISTAS:)
    ordenantiguas = merge.sort(antiguas,cmpdate)
    ordencostosas = merge.sort(costosas,cmpcost)
    tuplatriple = costoretotal,ordenantiguas,ordencostosas,pesototal
    return tuplatriple

def funcionReqUnoReto(catalog, inicial, final):
    ini = int(float(inicial))
    fin = int(float(final))
    tad_rta = lt.newList("ARRAY_LIST")
    for i in range(ini,fin+1):
        anio = mp.get(catalog['yearsborn'], i)
        if anio:
            artistas = me.getValue(anio)
            a_pasar=artistas["artists"]
            for x in range(1, lt.size(a_pasar)+1):
                elem= lt.getElement(a_pasar,x)
                lt.addLast(tad_rta, elem)
    return tad_rta

def ReqDos(catalog, inicial, final):
    ini = int(inicial[0:4])
    fin = int(final[0:4])
    data = lt.newList("ARRAY_LIST")
    purhcased = 0

    for i in range(ini, fin+1):

        if i == ini or i == fin:
            anio = mp.get(catalog["DateAcquired"], str(i))
            if anio:
                anio = me.getValue(anio)
                for x in range(1, lt.size(anio)+1):
                    ele = lt.getElement(anio, x)

                    if ele["DateAcquired"] >= inicial and ele["DateAcquired"] <= final:

                        if "purchase" in ele["CreditLine"].lower():
                            purhcased += 1 

                        autores = "-"
                        au = ele["ConstituentID"].replace("[", "").replace("]", "").replace(" ", "").split(",")
                        for a in au:
                            art = mp.get(catalog["ArtistConstituent"], a)
                            if art:
                                arti = me.getValue(art)
                                autores = autores + arti["DisplayName"] + "-"

                        ele["ConstituentID"] = autores
                        lt.addLast(data, ele)
        else:
            anio = mp.get(catalog["DateAcquired"], str(i))
            if anio:
                obras = me.getValue(anio)
                for j in range(1, lt.size(obras)+1):
                    ele = lt.getElement(obras, j)

                    if "purchase" in ele["CreditLine"].lower():
                        purhcased += 1 

                    autores = "-"
                    au = ele["ConstituentID"].replace("[", "").replace("]", "").replace(" ", "").split(",")
                    for a in au:
                        art = mp.get(catalog["ArtistConstituent"], a)
                        if art:
                            arti = me.getValue(art)
                            autores = autores + arti["DisplayName"] + "-"
                    ele["ConstituentID"] = autores
                    lt.addLast(data, ele)

    data = merge.sort(data, cmpdateadquired)

    return [data, purhcased]

def funcionReqTres(catalog, nombre):
    autor = mp.get(catalog['ArtistConsti'], nombre)
    autor = me.getValue(autor)
    sinorden= autor['ltrequetres']
    ordenado= merge.sort(sinorden,cmpcount)
    elmapa = autor["requetres"]
    contador = 0
    for i in range(1,lt.size(ordenado)+1):
        ele= lt.getElement(ordenado,i)
        contador+= ele['Cant']
    tuplarta = ordenado, elmapa, contador
    return tuplarta

def ReqCuatro(catalog):

    nationality = catalog["Nationality"]

    keys = mp.keySet(nationality)
    keys = lt.iterator(keys)
    data = lt.newList("ARRAY_LIST")

    for i in keys:
        elem = mp.get(nationality, i)
        elem = me.getValue(elem)
        size = lt.size(elem)

        nat = {"Nationality": i,
               "size": size,
               "Artworks": elem}

        lt.addLast(data, nat)

    return merge.sort(data, cmpsize)


def cmpFunctionRuno(anouno, anodos):
    return (int(anouno["BeginDate"]) < int(anodos["BeginDate"]))

def cmpobjectid(iduno, iddos):
    return (int(iduno["ObjectID"]) < int(iddos["ObjectID"]))

def cmpFunctionIndice(artist1, artist2):
    return (int(artist1["ConstituentID"]) < int(artist2["ConstituentID"]))

def cmpcount(countuno, countdos):
    return (int(countuno["Cant"])> int(countdos["Cant"]))

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
    return int(obras1["size"]) > int(obras2["size"])

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


def cmpdateadquired(obras1, obras2):
    return int(obras1["DateAcquired"].replace("-", "")) < int(obras2["DateAcquired"].replace("-", ""))