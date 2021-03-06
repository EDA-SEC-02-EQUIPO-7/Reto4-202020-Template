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
from DISClib.ADT import queue
import timeit
assert config
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

BikesFiles = "201801-1-citibike-tripdata.csv"
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
    print("3- Consultar si dos vertices pertenecen a un mismo cluster ")
    print("4- Consultar rutas cíclicas  ")
    print("5- Consultar rutas Criticas")
    print("6- Consular rutas segun resistencia")
    print("7- Recomendador de rutas  ")
    print("8- Interes Turistico ")
    print ("10-Identificación de Estaciones para Publicidad  ")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de rutas de citibikes ....")
    total_trips = (controller.loadFile(cont, BikesFiles))[1]
    print ("El nuemro de componentes fuertemente Conectados es {}".format(controller.numero_SCC(cont["grafo"])))
    print ("El numero de Estaciones cargadas es {}".format(controller.totalStations(cont)))
    print ("El numero Conecciones cargadas es {}".format(controller.totalConnections(cont)))
    print ("El numero de viajes cargados es de {} ".format(total_trips))
    #print ( cont["tablesalida"])
    
    
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
    
    verticeCentral = input ("Ingrese la estación para la cual desea realizar la consulta (Ejemplo 3661, 477): ")
    LimiteInferior = (int (input("Ingrese el limite inferior del rango a consultar (Ej 120): "))) * 60
    LimiteSuperior = (int (input("Ingrese el limite superior del rango a consultar (Ej 240): "))) * 60
    
    listaAdyacentes = controller.ListaAdyacentes(cont, verticeCentral, LimiteInferior, LimiteSuperior)

    print ("\nSe encontraron en total {} rutas cíclicas:\n " .format(listaAdyacentes[0]))
    
    while (not stack.isEmpty(listaAdyacentes[1])): 
        stop = stack.pop(listaAdyacentes[1])
        print ("Esta ruta tarda en total {} minutos, tiene {} estaciones, teniendo en cuenta un tiempo de 20 minutos por estacion. " .format((round((stop["PesoPorRuta"]/60), 2)), str(queue.size(stop)), ))
        while stop and (not queue.isEmpty(stop)):
            stopDOS = queue.dequeue(stop)
            print("-> Parte de la estacion {}, hasta la estación {} y tarda {} minutos en el trayecto. " .format( stopDOS['vertexA'],stopDOS['vertexB'], round((stopDOS['weight']/60), 2)))
        print ("\n")


def optionSix ():
    initialStation = input("Escriba la estacion de inicio del trayecto: ")
    limite = input("Escriba la duracion deseada del trayecto: ")
    lstpaths = it.newIterator(controller.rutasPorResistencia(cont,initialStation, int(limite)))
    while it.hasNext(lstpaths):
        eachPath = it.next(lstpaths )
        print("Estacion de partida {} ---- Estacion de llegada {} ----- Duracion {} ".format(eachPath["Initial Station"], eachPath["Final Station"], eachPath["Time"]))

def optionFive ():
    topStations = controller.critical_Station(cont)
    tops = it.newIterator(topStations["listllegada"])
    print ("-----------------------------------------")
    num=1
    while it.hasNext(tops):
        eachtop = it.next(tops)
        print ("La estacion Top {} de llegada es: {}".format(num,eachtop))
        num+=1
    print ("-----------------------------------------")
    num=1
    out = it.newIterator(topStations["listsalida"])
    while it.hasNext(out):
        eachtop = it.next(out)
        print ("La estaciones Top {} de Salida es: {}".format(num,eachtop))
        num+=1
    print ("-----------------------------------------")
    num=1
    less = it.newIterator(topStations["listuso"])
    while it.hasNext(less):
        eachtop = it.next(less)
        print ("La estacion Top {} de Menos uso es: {}".format(num,eachtop))
        num+=1
    #NO BORRAR LO COMENTADO ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    """
    print ("\nSe encontraron en total {} rutas cíclicas:\n " .format(listaAdyacentes[0]))
    while (not stack.isEmpty(listaAdyacentes[1])): 
        stop = stack.pop(listaAdyacentes[1])
        print ("Esta ruta tiene en total {} estaciones, teniendo en cuenta un tiempo de 20 minutos por estacion sumado al tiempo estimado de recorrido, este camino tarda en total {} minutos" .format(str(stack.size(stop)), (round((stop["PesoTotal"]/60), 2))))
        while (not stack.isEmpty(stop)):
            stopDOS = stack.pop(stop)
            print("-> Parte de la estacion {}, hasta la estación {} y tarda {} minutos en el trayecto. " .format( stopDOS['vertexA'],stopDOS['vertexB'], round((stopDOS['weight']/60), 2)))
        print ("\n")
        """

    #NO BORRAR LO COMENTADO ↑↑↑↑↑↑↑↑

def optioneigth():
    strlat = input("Escriba la latitud de inicio")
    strlon = input("Escriba la longitud de inicio")
    endlat = input("Escriba la latitud de llegada")
    endlon = input("Escriba la longitud de llegada")
    lstiterator =(controller.touristInterestPath(cont,strlat,strlon,endlat,endlon))
    try:
        if lstiterator["type"]== 'SINGLE_LINKED' or lstiterator["type"]== 'ARRAYLIST':
            while not stack.isEmpty(lstiterator):
                each = stack.pop(lstiterator)
                print ("La ruta de interes turstico para las cordenadas inicia en la estacion {} hasta \nla estacion {} con una duración de {} minutos".format(each["vertexA"],each["vertexB"],each['weight']))
    except: 
        print("Entre la estacion "+lstiterator["start"]+" y la estacion "+lstiterator["end"]+ " No se encontro una ruta")

def optionSeven():
    edad = input("Escriba edad para generar una ruta recomendada: ")
    recommendedPath = controller.recommendedPaths(cont,edad)
    lstIterator = it.newIterator(recommendedPath)
    if recommendedPath==None:
        print("no existe ruta")
    else:
        while it.hasNext(lstIterator):
            each = it.next(lstIterator)
            print (("la Ruta recomendada para la edad de {} años, va desde la estacion {} a la estacion {} con una duracion de {} minutos".format(edad,each["vertexA"],each["vertexB"],each['weight'] )))


def optionNine():
    
    identificadorproblema = input ("Ingrese el número de la bicicleta a consultar (Ejemplo 33319, 31956): ")
    fechaproblema = input("Ingrese la fecha que desee consultar (Ej 2018-01-21; 2018-01-11): ")

    RequiereMantenimiento = controller.MantenimientoBicicletas(cont, identificadorproblema, fechaproblema)

    print ("El día {}, La bicicleta identificada con el número {}, ha sido usada en total {} minutos, mientras ha estado estacionada {} minutos en total. ".format(fechaproblema, identificadorproblema, str(round  ( ( RequiereMantenimiento['SegundosUsada'] / 60), 2)), str(round  ( ( RequiereMantenimiento['SegundosParqueada'] / 60), 2))))                                   
    print ("Los viajes que se han registrado son: ")

    while (not stack.isEmpty(RequiereMantenimiento["RecorridosRealizados"])): 
        stop = stack.pop(RequiereMantenimiento["RecorridosRealizados"])
        print ("punto de partida {}, llegó a {}. ".format(stop[0], stop[1]))

def optionTen():
    edad = input("Escriba edad para generar una ruta recomendada: ")
    recommendedPath = controller.recommendedPathsBono(cont,edad)
    lstIterator = it.newIterator(recommendedPath)
    while it.hasNext(lstIterator):
        it.next(lstIterator)
        each = it.next(lstIterator)
        while (not stack.isEmpty(each)): 
            stop = stack.pop(each)
        print (("es el par de estaciones  {} y {} ".format(stop["vertexA"],stop["vertexB"] )))
  
    

#Menu principal

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
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

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime)) 

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optioneigth, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        sys.exit(0)
    else:
        sys.exit(0)
sys.exit(0)


