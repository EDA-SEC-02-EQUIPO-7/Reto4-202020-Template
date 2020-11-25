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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def newAnalyzer():
    bikes=model.newAnalyzer()
    return bikes

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(bikes):
    for filename in cf.file_dir(cf.data_dir):    
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(bikes, filename)
    return bikes

def loadFile(bikes, tripfile):
    """
    """
    total_trips = 0
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(bikes, trip)
        total_trips += 1 
    return [bikes,total_trips]

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def numero_SCC(bikes):
    return model.numSCC(bikes)

def SameCluster (bikes, VerticeA, VerticeB):
    return model.SameCluster(bikes, VerticeA, VerticeB)

def totalStations(bikes):
    return model.totalStations(bikes)

def totalConnections(bikes):
    return model.totalConnections(bikes)

def requerimiento3(bikes):
    return model.requerimiento3(bikes)


def requerimiento6(bikes,strlat,strlon,endlat,endlon):
    strcoord={"lat":None,
            "lon":None}
    endcoord={"lat":None,
            "lon":None}
    strcoord["lat"]=(strlat)
    strcoord["lon"]=(strlon)
    endcoord["lat"]=(endlat)
    endcoord["lon"]=(endlon)
    return model.rutarecomendada(bikes,strcoord,endcoord)
def requerimiento5(bikes,edad):
    return model.requerimiento5(bikes,edad)



def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def ListaAdyacentes (analyzer, vertice, inferior, superior):
    return model.ConsultaRutasCirculares(analyzer, vertice, inferior, superior)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)
