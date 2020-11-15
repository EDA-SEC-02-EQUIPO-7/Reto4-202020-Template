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
    return bikes

# Funciones para agregar informacion al grafo
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
    return bikes

def addConnection(bikes, origin , destination , duration):
    edge=gr.getEdge(bikes["grafo"],origin,destination)
    if edge is None:
        gr.addEdge(bikes["grafo"],origin,destination,duration)
    else:
        initial =edge["weight"]
        edge["weight"]=((int(initial)+int(duration))/2)
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



def ConsultaRutasCirculares (bikes, vertice):

    #consulta de lista de adyacentes al vertice problema
    #AplicaDijsktra = minimumCostPaths(bikes, vertice)


    ListaCompleta = ListaAdyacentes(bikes, vertice)
    lstiterator=it.newIterator(ListaCompleta)
    conteoCaminos = 0


    #search = minimumCostPaths(bikes, vertice)

    #search = DepthFirstSearch(bikes["grafo"], vertice)
    
    """
    while (not stack.isEmpty(pilaDFS)): 

        stop = stack.pop(pilaDFS)
        #TimpoPorAdyacentes += float(stop["weight"])
        print(stop)
        """

    while it.hasNext(lstiterator):
        eachaStation=it.next(lstiterator)



        minimumCostPaths(bikes, vertice)
        FirsPath = minimumCostPath(bikes, eachaStation)
        Firststop = stack.pop(FirsPath)                

        
        minimumCostPaths(bikes, eachaStation)
        SecondPath = minimumCostPath(bikes, vertice)

        
        """if SecondPath is not None:
            stack.push(SecondPath, Firststop)
            stop = stack.pop(SecondPath)
            TimpoPorAdyacentes += float(stop["weight"])
            print(stop)"""
        



        if SecondPath is not None:
            stack.push(SecondPath, Firststop)
            conteoCaminos += 1
            pathlen = stack.size(SecondPath)
            print('El camino encontrado tiene en total {} estaciones: ' .format(str(pathlen + 1)))

            TiempoTotalCadaRecorrido = 0   
            TimpoPorAdyacentes = 0         
            #print (Firststop)
            while (not stack.isEmpty(SecondPath)): 

                stop = stack.pop(SecondPath)
                TimpoPorAdyacentes += float(stop["weight"])
                print(stop)

            TiempoTotalCadaRecorrido = float(Firststop["weight"]) + TimpoPorAdyacentes + (pathlen*20*60)
            TiempoTotalCadaRecorrido = (round((TiempoTotalCadaRecorrido/60),2))
            print ("El tiempo total del recorrido, incluyendo tiempo de los trayectos y un tiempo aproximado de 20 minutos de recorrido turístico en cada estacion, es de {} minutos: " .format(str(TiempoTotalCadaRecorrido)))

            print ("\n")


    print ("el total de caminos encontrados fue de: " + str (conteoCaminos))

    

    
    

    


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

        
def ListaAdyacentes (bikes, vertice):

    #consulta de lista de adyacentes al vertice problema
    return gr.adjacents(bikes['grafo'], vertice)

def DepthFirstSearch(graph, source):
    return dfs.DepthFirstSearch(graph, source)

def DFS_pathTo(search, vertex):
    return dfs.pathTo(search, vertex)




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

