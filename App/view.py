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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

BikesFiles = "201801-3-citibike-tripdata.csv"
initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido al servicio de consulta de CitiBikes\nEstas son las consultas que puede realizar:\n")
    print("1- Inicializar Analizador")
    print("2- Cargar información de rutas")
    print("3- Consultar si dos vertices pertenecen a un mismo cluster (Requerimiento 1)")
    print("4- Establecer parada base:")
    print("5- Requerimiento x ")
    print("6- Requerimiento y ")
    print("7- Requerimiento z ")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de rutas de citibikes ....")
    total_trips = (controller.loadFile(cont, BikesFiles))[1]
    print ("El nuemro de componentes fuertemente Conectados es {}".format(controller.numero_SCC(cont["grafo"])))
    print ("El numero de Estaciones cargadas es {}".format(controller.totalStations(cont)))
    print ("El numero Conecciones cargadas es {}".format(controller.totalConnections(cont)))
    print ("El numero de viajes cargados es de {} ".format(total_trips))
    

def optionThree():
    #Determinar si dos estaciones pertenecen a un mismo cluster
    print ("\nIngrese el nombre de las dos estaciones que desea consultar:")
    Vertice_A = input("Nombre de la estacion #1: ")
    Vertice_B = input("Nombre de la estacion #2: ")
    SameCluster = controller.SameCluster(cont["grafo"], Vertice_A, Vertice_B)
    if SameCluster:
        print ("Las estaciones {} y {} pertenecen al mismo cluster".format(Vertice_A,Vertice_B))
    else: 
        print ("Las estaciones {} y {} NO pertenecen al mismo cluster".format(Vertice_A,Vertice_B))

def optionFour():
    
    verticeCentral = input ("Ingrese la estación para la cual desea realizar la consulta: ")
    controller.minimumCostPaths(cont, verticeCentral)
    listaAdyacentes = controller.ListaAdyacentes(cont, verticeCentral)
    #controller.minimumCostPath(cont, verticeCentral)

    """path = controller.minimumCostPath(cont, verticeCentral)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)"""
    

    

#Menu principal

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.newAnalyzer()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        #optionTwo()

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    
    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    else:
        sys.exit(0)
sys.exit(0)
