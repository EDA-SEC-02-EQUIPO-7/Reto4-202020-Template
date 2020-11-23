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
from DISClib.ADT import indexminpq as iminpq
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
        'paths': None
    }
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
    return bikes

def addTrip(bikes,trip):
    origin=trip["start station id"]
    destination=trip["end station id"]
    duration=int(trip['tripduration'])
    addStation(bikes, origin)
    addStation(bikes, destination)
    addConnection(bikes, origin, destination, duration)

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
    oruseinv=1/oruse
    desuseinv=1/desuse
    llegadainv=1/llegada
    salidainv=1/salida
    iminpq.decreaseKey(bikes["topuso"], destination,desuseinv)
    iminpq.decreaseKey(bikes["topuso"], origin,oruseinv)
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
