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

BikesFiles = "201801-4-citibike-tripdata.csv"
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
    print("3- Calcular componentes conectados")
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
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))

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
        optionTwo()

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
