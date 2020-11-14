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

def ListaAdyacentes (bikes, vertice):

    #consulta de lista de adyacentes al vertice problema
    ListaCompleta = gr.adjacents(bikes['grafo'], vertice)

    lstiterator=it.newIterator(ListaCompleta)
    conteoCaminos = 0
    while it.hasNext(lstiterator):
        eachaStation=it.next(lstiterator)
        
        existeCaminoRegreso = djk.hasPathTo(eachaStation, vertice)
        print (existeCaminoRegreso)
        #conteoCaminos += 1
        #print (conteoCaminos)

        #a partir de la lista de posibles caminos, se calcula la ruta a tomar en cada caso
"""
        path = minimumCostPath(bikes, vertice)
        if path is not None:
            pathlen = stack.size(path)
            print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
"""

def minimumCostPath(bikes, vertice):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(bikes['paths'], vertice)
    return path

        






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

