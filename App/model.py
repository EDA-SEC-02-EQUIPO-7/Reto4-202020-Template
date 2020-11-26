"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.DataStructures import mapentry as me
from math import radians, cos, sin, asin, sqrt ,degrees,atan2
from DISClib.ADT import indexminpq as iminpq
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
from DISClib.Algorithms.Graphs import scc
from DISClib.ADT import stack
from DISClib.ADT import queue
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    bikes = {
        "Stations":None,
        "Trips":None,
        "grafo": None,
        'paths': None,
        "table":None}
    bikes["grafo"]=gr.newGraph(datastructure="ADJ_LIST",
                            directed=True,
                            size=1000,
                            comparefunction=compareStations)
    bikes["topsalida"]=iminpq.newIndexMinPQ(
                                  cmpfunction=cmpimin
                                  )
    bikes["topllegada"]=iminpq.newIndexMinPQ(
                                  cmpfunction=cmpimin
                                   )
    bikes["topuso"]=iminpq.newIndexMinPQ(
                                  cmpfunction=cmpimin
                                   )
    bikes["stationtree"]= om.newMap(omaptype='',
                                      comparefunction=comparebycoord)
    bikes["tablesalida"]= m.newMap(maptype='',
                                      comparefunction=compareIds)
    bikes["tablellegada"]= m.newMap(maptype='',
                                      comparefunction=compareIds)
    bikes["mayoressalida"]=m.newMap(maptype='',
                                      comparefunction=compareIds)
    bikes["mayoresllegada"]=m.newMap(maptype='',
                                      comparefunction=compareIds)
    bikes["names"]=m.newMap(maptype='',
                                      comparefunction=compareIds)
    return bikes

def addTrip(bikes,trip):
    origin=trip["start station id"]
    destination=trip["end station id"]
    duration=int(trip['tripduration'])
    addStation(bikes, origin)
    addStation(bikes, destination)
    addConnection(bikes, origin, destination, duration)
    updateCoordIndex(bikes["stationtree"],trip)
    addidname(bikes["names"],trip)
    age=changeyear(trip["birth year"])
    exi=m.contains(bikes["tablesalida"],trip["start station id"])
    if exi:
        entry=m.get(bikes["tablesalida"],trip["start station id"])
        ages=me.getValue(entry)
        exi=m.contains(ages,age)
        if exi:
            entry=m.get(ages,age)
            part=me.getValue(entry)
            m.put(ages,age,part+1)
        else:
            m.put(ages,age,1)
    else:
        ages=m.newMap(maptype='',comparefunction=compareIds)
        m.put(bikes["tablesalida"],trip["start station id"],ages)
        entry=m.get(bikes["tablesalida"],trip["start station id"])
        ages=me.getValue(entry)
        m.put(ages,age,1)
    entry=m.get(bikes["tablesalida"],trip["start station id"])
    ages=me.getValue(entry)
    cant=m.get(ages,age)
    num=me.getValue(cant)
    exi=m.contains(bikes["mayoressalida"],age)
    if exi:
        mayor=entry=m.get(bikes["mayoressalida"],age)
        vertex=me.getValue(mayor)
        numero=vertex["cantidad"]
        if numero<num:
            m.put(bikes["mayoressalida"],age,{"vertex":trip["start station id"],"cantidad":num})
            entry=m.get(bikes["mayoressalida"],age)
    else:
        m.put(bikes["mayoressalida"],age,{"vertex":trip["start station id"],"cantidad":num})
        entry=m.get(bikes["mayoressalida"],age)
    
    exi=m.contains(bikes["tablellegada"],trip["end station id"])
    if exi:
        entry=m.get(bikes["tablellegada"],trip["end station id"])
        ages=me.getValue(entry)
        exi=m.contains(ages,age)
        if exi:
            entry=m.get(ages,age)
            part=me.getValue(entry)
            m.put(ages,age,part+1)
        else:
            m.put(ages,age,1)
    else:
        ages=m.newMap(maptype='',comparefunction=compareIds)
        m.put(bikes["tablellegada"],trip["end station id"],ages)
        entry=m.get(bikes["tablellegada"],trip["end station id"])
        ages=me.getValue(entry)
        m.put(ages,age,1)
    entry=m.get(bikes["tablellegada"],trip["end station id"])
    ages=me.getValue(entry)
    cant=m.get(ages,age)
    num=me.getValue(cant)
    exi=m.contains(bikes["mayoresllegada"],age)
    if exi:
        mayor=entry=m.get(bikes["mayoresllegada"],age)
        vertex=me.getValue(mayor)
        numero=vertex["cantidad"]
        if numero<num:
            m.put(bikes["mayoresllegada"],age,{"vertex":trip["end station id"],"cantidad":num})
            entry=m.get(bikes["mayoresllegada"],age)
    else:
        m.put(bikes["mayoresllegada"],age,{"vertex":trip["end station id"],"cantidad":num})
        entry=m.get(bikes["mayoresllegada"],age)
    

def addidname(map,trip):
    exi=m.contains(map,trip["start station id"])
    if exi ==False:
        m.put(map,trip["start station id"],"start station name")
    exi=m.contains(map,trip["end station id"])
    if exi ==False:
        m.put(map,trip["end station id"],"end station name")

    

def updateCoordIndex(map,trip):
    occurredCoord ={"lat":float(trip["start station latitude"]),"lon":float(trip["start station longitude"]),"id":float(trip["start station id"])}
    entry=om.get(map,occurredCoord)
    if entry is None:
        coordentry =newDataEntryBono(trip)
        om.put(map,occurredCoord,coordentry)
    else:
        coordentry=me.getValue(entry)
    addCoord(coordentry,trip)
    occurredCoord ={"lat":float(trip["end station latitude"]),"lon":float(trip["end station longitude"]),"id":float(trip["end station id"])}
    entry=om.get(map,occurredCoord)
    if entry is None:
        coordentry =newDataEntryBono(trip)
        om.put(map,occurredCoord,coordentry)
    else:
        coordentry=me.getValue(entry)
    addCoord(coordentry,trip)
    return map

def addCoord(coordentry,trip):
    lst=coordentry["lst"]
    lt.addLast(lst,trip)

def newDataEntryBono(accident):
    entry={"lst":None}
    entry["lst"]=lt.newList("SINGLE_LINKED",comparebycoord)
    return entry
def addStation(bikes,stationid):
    if not gr.containsVertex(bikes["grafo"],stationid):
        gr.insertVertex(bikes["grafo"],stationid)
        iminpq.insert(bikes["topsalida"],stationid,1)
        iminpq.insert(bikes["topllegada"],stationid,1)
        iminpq.insert(bikes["topuso"],stationid,1)
    return bikes

def addConnection(bikes, origin , destination , duration):
    edge=gr.getEdge(bikes["grafo"],origin,destination)
    if edge is None:
        gr.addEdge(bikes["grafo"],origin,destination,duration)
    else:
        initial =edge["weight"]
        edge["weight"]=((int(initial)+int(duration))/2)
    llegada=gr.indegree(bikes["grafo"],destination)
    salida=gr.outdegree(bikes["grafo"],origin)
    llegadad=gr.indegree(bikes["grafo"],destination)
    salidad=salida=gr.outdegree(bikes["grafo"],origin)
    oruse=salida+llegadad
    desuse=llegada+salidad
    llegadainv=1/llegada
    salidainv=1/salida
    iminpq.increaseKey(bikes["topuso"], destination,desuse)
    iminpq.increaseKey(bikes["topuso"], origin,oruse)
    iminpq.decreaseKey(bikes["topllegada"], destination,llegadainv)
    iminpq.decreaseKey(bikes["topsalida"], origin, salidainv)
    return bikes


    

# ==============================
# Funciones de requerimientos
# ==============================


#Requerimiento 2


def minimumCostPaths(bikes, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    bikes['paths'] = djk.Dijkstra(bikes['grafo'], initialStation)
    return bikes


def BreadhtFisrtSearch(graph, source):
    bfs.BreadhtFisrtSearch(graph, source)

def BFS_PathTo(search, vertex):
    bfs.pathTo(search, vertex)



def ConsultaRutasCirculares (bikes, vertice, inferior, superior):

    ListaCompleta = ListaAdyacentes(bikes, vertice)
    lstiterator=it.newIterator(ListaCompleta)
    conteoCaminos = 0

    stackfinal = stack.newStack()
    CadaRuta = queue.newQueue()
    ConteoDeRutas = 0


    while it.hasNext(lstiterator):
        eachaStation=it.next(lstiterator)

        primerRecorrido = getEdge(bikes['grafo'], vertice, eachaStation)

        search = minimumCostPaths(bikes, eachaStation)
        colados = minimumCostPath(bikes, vertice)

        if colados and ((stack.size(colados))*60*20) < superior:
            pesoporestaciones = (stack.size(colados))*60*20
            pesocamino = 0
            pesoTOTALdos = pesoporestaciones + pesocamino + primerRecorrido['weight']

            CadaRuta = queue.newQueue()
            queue.enqueue(CadaRuta, primerRecorrido)

            while (not stack.isEmpty(colados)) and (pesoTOTALdos < superior):

                stopDOS = stack.pop(colados)
                pesoTOTALdos += stopDOS['weight']

                queue.enqueue(CadaRuta, stopDOS)

            
            if inferior < pesoTOTALdos < superior and CadaRuta:
                CadaRuta["PesoPorRuta"] = pesoTOTALdos
                ConteoDeRutas += 1
                stack.push(stackfinal, CadaRuta)
        
    return ConteoDeRutas, stackfinal

    #NO BORRAR LO COMENTADO ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    #NO BORRAR LO COMENTADO ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    #NO BORRAR LO COMENTADO ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    """
    #Req 2 funcionando
    #Req 2 funcionando
    #Req 2 funcionando


    ListaCompleta = ListaAdyacentes(bikes, vertice)
    lstiterator=it.newIterator(ListaCompleta)
    conteoCaminos = 0

    stackfinal = stack.newStack()

    
    while it.hasNext(lstiterator):
        eachaStation=it.next(lstiterator)

        primero = minimumCostPaths(bikes, vertice)
        primerpeso = distTo(primero, eachaStation)
        FirsPath = minimumCostPath(primero, eachaStation)
        Firststop = stack.pop(FirsPath)


        segundo = minimumCostPaths(bikes, eachaStation)
        SecondPath = minimumCostPath(bikes, vertice)
        if SecondPath:
            
            pesoconjunto = (distTo(segundo, vertice)) + primerpeso

            
            stack.push(SecondPath, Firststop)

            pathlen = stack.size(SecondPath)
            pesofinal = pesoconjunto + (pathlen*20*60)
                
            if inferior < pesofinal < superior:
                
                conteoCaminos += 1
                SecondPath["PesoTotal"]=pesofinal
                stack.push(stackfinal, SecondPath)

    
    return conteoCaminos, stackfinal
    """


    """
    ListaCompleta = ListaAdyacentes(bikes, vertice)
    lstiterator=it.newIterator(ListaCompleta)
    conteoCaminos = 0

    stackfinal = stack.newStack()
    CadaRuta = queue.newQueue()
    ConteoDeRutas = 0

    colauno = stack.newStack()
    stack.push(colauno, vertice)

    while it.hasNext(lstiterator):
        eachaStation=it.next(lstiterator)
        search = DepthFirstSearch(bikes['grafo'], eachaStation)
        colados = DFS_pathTo(search, vertice)

        if colados and ((stack.size(colados))*60*20) < superior:
            pesoporestaciones = (stack.size(colados))*60*20
            pesocamino = 0
            pesoTOTALdos = pesoporestaciones + pesocamino

            CadaRuta = queue.newQueue()

            while (not stack.isEmpty(colados)) and (pesoTOTALdos < superior):

                stopuno = stack.pop(colauno)
                stopDOS = stack.pop(colados)
                cadacamino = getEdge(bikes['grafo'], stopuno, stopDOS)
                
                stack.push(colauno, stopDOS)
                                
                if cadacamino:
                    pesoTOTALdos += cadacamino['weight']

                    queue.enqueue(CadaRuta, cadacamino)

            
            if inferior < pesoTOTALdos < superior and CadaRuta:
                CadaRuta["PesoPorRuta"] = pesoTOTALdos
                ConteoDeRutas += 1
                stack.push(stackfinal, CadaRuta)
        
    return ConteoDeRutas, stackfinal
    """
    #NO BORRAR LO COMENTADO ↑↑↑↑↑↑↑↑
    #NO BORRAR LO COMENTADO ↑↑↑↑↑↑↑↑
    #NO BORRAR LO COMENTADO ↑↑↑↑↑↑↑↑
#requerimiento 6
#requerimiento 6
#requerimiento 6
#requerimiento 6
#requerimiento 6
def rutarecomendada(bikes,strcoord,endcoord):
    rbt=bikes["stationtree"]
    values={"list":None}
    values["list"]=lt.newList('SINGLELINKED', rbt['cmpfunction'])
    distance=0.01
    while lt.size(values["list"])==0:
        values= keyrange(rbt['root'], lat(-distance,float(strcoord["lat"])), lat(distance,float(strcoord["lat"])),values,strcoord,distance)
        distance+=0.01
    estacioninicio=str(int(lt.getElement(values["list"],1)["id"]))
    values["list"]=lt.newList('SINGLELINKED', rbt['cmpfunction'])
    distance=0.01
    while lt.size(values["list"])==0:
        values= keyrange(rbt['root'], lat(-distance,float(endcoord["lat"])), lat(distance,float(endcoord["lat"])),values,endcoord,distance)
        distance+=0.01
    estacionfinal=str(int(lt.getElement(values["list"],1)["id"]))
    dijsktra=djk.Dijkstra(bikes["grafo"],estacioninicio)
    if djk.hasPathTo(dijsktra,estacionfinal):
        path=djk.pathTo(dijsktra,estacionfinal)
        print(path)
    else:
        print("ñoquis")
def keyrange(root,keylo ,keyhi,values,coord,distance):
    if (root is not None):
        y=float((root["key"]["lat"]))
        z=float(root["key"]["lon"])
        x=float(coord["lat"])
        w=float(coord["lon"])
        if (root["key"]["lat"] > keylo):
            keyrange(root['left'], keylo, keyhi, values,coord,distance)
        if (haversine(z,y,w,x)<=distance and root["key"]["lat"] > keylo and root["key"]["lat"] < keyhi):
            lt.addLast(values["list"],root["key"]) 
        if (root["key"]["lat"] < keyhi):
            keyrange(root['right'], keylo, keyhi, values,coord,distance)
    return values

def rutasPorResistencia(bikes,initialStation,Limit):
    LimitPaths = lt.newList("ARRAY_LIST")
    shortParths = minimumCostPaths(bikes,initialStation)
    stations = shortParths["paths"] ['visited']
    desIterator =it.newIterator(ph.keySet(stations))
    while it.hasNext(desIterator):
        eachdesination = it.next(desIterator)
        shortParth  = minimumCostPath(shortParths,eachdesination)
        while not stack.isEmpty(shortParth):
            eachPath = stack.pop(shortParth)
            if int(eachPath["weight"]) <= Limit:
                lt.addLast(LimitPaths, {"Initial Station":eachPath['vertexA'], "Final Station":eachPath['vertexB'], "Time":eachPath'weight'})
    return (LimitPaths)
    
#requerimiento 3
#requerimiento 3
#requerimiento 3
#requerimiento 3
def requerimiento3(bikes):
    retorno={"listuso":None,
                "listsalida":None,
                "listllegada":None}
    retorno["listuso"]=lt.newList('SINGLELINKED', comparevalues)
    retorno["listsalida"]=lt.newList('SINGLELINKED', comparevalues)
    retorno["listllegada"]=lt.newList('SINGLELINKED', comparevalues)
    while lt.size(retorno["listuso"])<3:
        x=iminpq.delMin(bikes["topuso"])
        lt.addLast(retorno["listuso"],x)
    print("--------------------------------------------")
    print(retorno["listuso"])
    while lt.size(retorno["listsalida"])<3:
        x=iminpq.delMin(bikes["topsalida"])
        lt.addLast(retorno["listsalida"],x)
    print("--------------------------------------------")
    print(retorno["listsalida"])
    while lt.size(retorno["listllegada"])<3:
        x=iminpq.delMin(bikes["topllegada"])
        lt.addLast(retorno["listllegada"],x)
    print("--------------------------------------------")
    print(retorno["listllegada"])

    return retorno
#requerimiento 5
#requerimiento 5
#requerimiento 5
#requerimiento 5
def requerimiento5(bikes,edad):
    old=changeyear(edad)
    entry=m.get(bikes["mayoressalida"],old)
    print(entry)
    value=me.getValue(entry)
    vertex1=value["vertex"]
    entry=m.get(bikes["mayoresllegada"],old)
    print(entry)
    value=me.getValue(entry)
    vertex2=value["vertex"]
    dijsktra=djk.Dijkstra(bikes["grafo"],vertex1)
    if djk.hasPathTo(dijsktra,vertex2):
        path=djk.pathTo(dijsktra,vertex2)
        print(path)
    else:
        print("ñoquis")




def minimumCostPath(bikes, vertice):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(bikes['paths'], vertice)
    return path


def hasPath(bikes, vertice):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(bikes['paths'], vertice)

def distTo(search, vertex):
    return djk.distTo(search['paths'], vertex)

        
def ListaAdyacentes (bikes, vertice):

    #consulta de lista de adyacentes al vertice problema
    return gr.adjacents(bikes['grafo'], vertice)

def DepthFirstSearch(graph, source):
    return dfs.DepthFirstSearch(graph, source)

def DFS_pathTo(search, vertex):
    return dfs.pathTo(search, vertex)

def getEdge(graph, vertexa, vertexb):
    return gr.getEdge(graph, vertexa, vertexb)




# ==============================
# Funciones de consulta
# ==============================


def numSCC(grafo):
    sc = scc.KosarajuSCC(grafo)
    return scc.connectedComponents(sc)

def SameCluster (grafo, VerticeA, VerticeB):
    sc = scc.KosarajuSCC(grafo)
    #print (sc["idscc"])
    return scc.stronglyConnected(sc, VerticeA, VerticeB)


def totalStations(bikes):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(bikes["grafo"])


def totalConnections(bikes):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(bikes["grafo"])






# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
def cmpimin(value1, value2):
    """
    Compara dos estaciones
    """
    value2 = value2['key']
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1
def comparebycoord(coord1,coord2):
    if coord1["lat"]==coord2["lat"]:
        return 0
    if coord1["lat"]>coord2["lat"]:
        return 1
    else:
        return -1
        
def haversine(lon1, lat1, lon2, lat2):
    lon1=radians(lon1)
    lat1=radians(lat1)
    lon2=radians(lon2)   
    lat2=radians(lat2)
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def lat(d,lat1):
    R = 6371 #Radius of the Earth
    brng =0 #Bearing is 90 degrees converted to radians.
    lat1 =radians(lat1) #Current lat point converted to radians
    lat2 = asin( sin(lat1)*cos(d/R) +
         cos(lat1)*sin(d/R)*cos(brng))
    
    lat2 =degrees(lat2)
    return lat2
def compareIds(id1, id2):
    """
    Compara dos accidentes por su id
    """
    id2 = id2['key']
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def changeyear(year):
    old=2020-int(year)
    if old>=0 and old <=10:
        old=0
    elif old>=11 and old <=20:
        old=11
    elif old>=21 and old <=30:
        old=21
    elif old>=31 and old <=40:
        old=31
    elif old>=41 and old <=50:
        old=41
    elif old>=51 and old <=60:
        old=51
    elif old>=60:
        old=60
    return old
def comparevalues(v1,v2):
    if (v1 == v2):
        return 0
    elif v1 > v2:
        return 1
    else:
        return -1