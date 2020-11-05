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

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    bikes["grafo"]=gr.newGraph(datastructure="AFJ_LIST",
                            directed=True,
                            size=1000
                            comparefunction=comareStations)

# Funciones para agregar informacion al grafo
def addTrip(analyzer,trip):
    origen=trip["'start station id"]
    duration=trip["'end station id"]
    daration=int((trip['tripduration']))
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)
def addStation(analyzer,stationid):
    if not gr.containsVertex(analyzer["grafo"],stationid):
        gr.insertVertex(analyzer["grafo"],stationid)
    return analyzer
def addConnection(analyzer, origin , destination , duration):
    edge=gr.getEdge(analyzer["grafo"],origin,destination)
    if edge is None:
        gr.addEdge(analyzer["grafo"],origin,destination,duration)
    else:
        initial=edge["weight"]
        edge["weight"]=((int(intitial)+int(duration))/2)
    

# ==============================
# Funciones de consulta
# ==============================

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================