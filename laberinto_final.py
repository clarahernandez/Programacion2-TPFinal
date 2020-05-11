import pytest

def eliminar_enter(laberinto):
    '''Función que recibe el laberinto y elimina el enter de cada reglon
    eliminar_enter: Lista de string -> None
    Recibe una lista de strings que representan un laberinto y elimina el '\n' de cada string.'''
    
    ANCHO = len(laberinto[0])
    ALTO = len(laberinto)
    ancho = len(laberinto[0])
    
    for i in range(0, len(laberinto)):
        laberinto[i] = laberinto[i][:(ancho-1)]
    return laberinto

def lector_coordenadas():
    '''Función que lee el archivo de coordenadas
    lector_coordenadas: None -> Lista de Strings
    La función no recibe nada. Abre el achivo donde se encuentran las coordenadas y
    devuelve el laberinto representado por una lista de strings. '''
    
    archivo = open('laberinto.txt','r')   #abre el archivo
    laberinto = archivo.readlines()
    archivo.close()
    
    laberinto = eliminar_enter(laberinto) #elimina el '\n' de cada fila
    
    return laberinto



def mover(pos_actual, direccion):
    '''Función que se mueve según la dirección
    mover: Tupla, String -> Tupla
    Recibe una tupla que representa la posición actual y un string que representa
    la dirección a donde se quiere ir. Devuelve una tupla que representa la nueva posición.'''
    
    if direccion == 'derecha':
        return (pos_actual[0],pos_actual[1]+1)
    elif direccion == 'izquierda':
        return (pos_actual[0], pos_actual[1]-1)
    elif direccion == 'arriba':
        return (pos_actual[0]-1, pos_actual[1])
    else:                                       #se mueve hacia abajo
        return (pos_actual[0]+1, pos_actual[1])

def mover_test():
    '''Función de prueba de mover'''
    assert mover((5,5),'derecha') == (5,6)
    assert mover((5,5),'izquierda') == (5,4)
    assert mover((5,5),'arriba') == (4,5)
    assert mover((5,5), '') == (6,5)
        

def puedo_mover(pos_actual,laberinto, ANCHO, ALTO):
    '''Función que nos dice cuantas veces nos podemos mover.
    puedo_mover: Tupla, Lista de Strings, Entero, Entero -> Entero
    Recibe una tupla que representa la posición actual, una lista de strings
    que representa a el laberinto, y dos enteros que representan cuantas columnas y filas hay en
    el laberinto. Devuelve un entero que representa cuantos posbiles movimientos hay desde
    la posición actual.'''

    i = 0 #contador de posibles movimientos

    derecha = mover(pos_actual, 'derecha')
    if  derecha[1] < ANCHO and laberinto[derecha[0]][derecha[1]] != '1' and laberinto[derecha[0]][derecha[1]] !='3':
        i = i+1
        

    izquierda = mover(pos_actual, 'izquierda')
    if  izquierda[1] >= 0 and laberinto[izquierda[0]][izquierda[1]] != '1' and laberinto[izquierda[0]][izquierda[1]] !='3':
        i = i+1

    arriba = mover(pos_actual, 'arriba')
    if arriba[0] >= 0  and arriba[1] <= ANCHO-1 and laberinto[arriba[0]][arriba[1]] != '1' and laberinto[arriba[0]][arriba[1]] != '3':
        i = i+1

    abajo = mover(pos_actual, 'abajo')
    if abajo[0] < ALTO and laberinto[abajo[0]][abajo[1]] != '1' and laberinto[abajo[0]][abajo[1]] != '3':
        i = i+1
        
    return i

def puedo_mover_test():
    '''Función de prueba de la funcion puedo_mover'''
    
    lab = [['030'],
           ['100'],
           ['000']]
    assert puedo_mover((0,0), lab, 3, 3) == 0
    assert puedo_mover((1,1), lab, 3, 3) == 2
    assert puedo_mover((2,1), lab, 3, 3) == 3
        


def avanzar(pos_actual, laberinto, ANCHO, ALTO):
    '''Función que hace que se mueva la posición actual.
    avanzar: Tupla, Lista de Strings, Entero, Entero -> Tupla
    Recibe una tupla que representa la posición actual, una lista de strings que representa
    al laberinto y dos enteros que representan cuantas columnas y filas hay en el laberinto.
    Devuelve una tupla que representa la posición a la que se puede avanzar.'''

    derecha = mover(pos_actual, 'derecha')
    izquierda = mover(pos_actual, 'izquierda')
    arriba = mover(pos_actual, 'arriba')
    abajo = mover(pos_actual, 'abajo')
    
    if  derecha[1] < ANCHO and laberinto[derecha[0]][derecha[1]] != '1' and laberinto[derecha[0]][derecha[1]] !='3':
        return derecha
    
    elif izquierda[1] >= 0 and laberinto[izquierda[0]][izquierda[1]] != '1' and laberinto[izquierda[0]][izquierda[1]] !='3':
        return izquierda
    
    elif arriba[0] >= 0  and arriba[1] <= ANCHO-1 and laberinto[arriba[0]][arriba[1]] != '1' and laberinto[arriba[0]][arriba[1]] != '3':
        return arriba
    
    else:    #si llego hasta acá es porque se puede mover por lo menos una vez
        return abajo
    

def avanzar_test():
    '''Función de prueba de la función avanzar'''

    laberinto = [['0010'],
                 ['0110'],
                 ['0101'],
                 ['0000']]
    
    assert avanzar((0,0), laberinto, 4, 4) == (0,1) #derecha
    assert avanzar((1,0), laberinto, 4, 4) == (0,0) #izquierda
    assert avanzar((1,3), laberinto, 4, 4) == (0,3) #arriba
    assert avanzar((2,2), laberinto, 4, 4) == (3,2) #abajo
    
    

def reemplazar_numeros(fila, posicion, ANCHO, caracter):
    '''Función que modifica una fila del laberinto en determinada posición.
    reemplazar_numeros: String, Entero, Entero, String -> String 
    Recibe un string que representa la fila del laberinto, un entero que representa la posición de la fila que
    queremos modificar, un entero que representa el largo 
    queremos poner a el número en la fila'''


    if posicion == ANCHO-1:            #si la posición está al final de la fila
        return fila[:posicion]+caracter
    elif posicion == 0:                #si la posición está al principio de la fila
        return caracter+fila[1:]
    else:
        return fila[:posicion]+caracter+fila[posicion+1:]
    
def resolver_laberinto(pos_actual, laberinto, camino, ANCHO, ALTO):
    '''Función que resuelve el laberinto.
    resolver_laberinto: Tupla, Lista de Strings, Lista de tuplas, Entero, Entero -> Lista de tuplas
    Recibe una tupla que representa la posición actual, una lista de strings que representa al laberinto,
    una lista de tuplas que representa el camino que fue haciendo y dos enteros que representan el tamaño del laberinto.'''

    longitud_camino = len(camino)
    
    if laberinto[pos_actual[0]][pos_actual[1]] == '2': 
        camino.append(pos_actual)
        solucion=camino[:]
        return solucion
    
    elif puedo_mover(pos_actual,laberinto, ANCHO, ALTO) == 0:  #si no me puedo mover
        
        if longitud_camino > 0: 
            laberinto[pos_actual[0]] = reemplazar_numeros(laberinto[pos_actual[0]], pos_actual[1], ANCHO, '1')
            return resolver_laberinto(camino[longitud_camino-1], laberinto, camino[:longitud_camino-1], ANCHO, ALTO)
        else:
            return []
    else:
        laberinto[pos_actual[0]] = reemplazar_numeros(laberinto[pos_actual[0]], pos_actual[1], ANCHO, '3')  #pone un 3 para saber que ya pasó por allí
        camino.append(pos_actual)
        return resolver_laberinto(avanzar(pos_actual,laberinto, ANCHO, ALTO),laberinto, camino, ANCHO, ALTO)

def resolver_laberinto_test():
    '''Función de prueba de la función resolver_laberinto'''

    assert resolver_laberinto((0,1), [['0210'],['0100']], [(0,0)], 4, 2) == [(0,0),(0,1)]
    assert resolver_laberinto((0,0), [['01'],['10']], [], 2,2) == []
    assert resolver_laberinto((0,0), [['0010'],['1001'],['1101'],['0121']], [], 4,4) == [(0,0), (0,1),(1,1),(2,1),(3,1)]

    
def escritor_solucion(solucion, ANCHO, ALTO):
   ''' Función que crea un archivo con la solucion.
   escritor_solucion: Lista de tuplas, Entero, Entero -> None
   Recibe una lista de tuplas que representa la solución del laberinto, y dos enteros que representan
   el tamaño de las columnas y de las filas del laberinto.
   Si la solución era una lista vacía crea un archivo con un espacio ('\n'). Si no, crea un archivo
   con cada uno de los pasos hasta el objetivo incluido. '''
   
   archivo = open('solucion.txt', 'w')
   if (solucion == []):  
      archivo.write(' ')
      print('El archivo no tiene solución')
   else:
       for i in range(len(solucion)):
            archivo.write(str(solucion[i][0]) + ' ' + str(solucion[i][1]) + '\n')
   archivo.close()
   print('El archivo se ha creado con éxito.')
   


def principal():
                                
    '''Función principal.
    principal: None -> None
    Lee un archivo con el laberinto y crea un archivo con los pasos que hay que seguir
    desde la posición de comienzo (0,0) hasta el objetivo.'''

    laberinto = lector_coordenadas()
    
    camino = []
    pos_actual = (0,0)
    ALTO = len(laberinto)
    ANCHO = len(laberinto[0])

    if laberinto[pos_actual[0]][pos_actual[1]] == '1' or puedo_mover(pos_actual,laberinto, ANCHO, ALTO) == 0: #Si hay una pared o no me puedo mover al principio.
        solucion = []
    else:
        solucion=resolver_laberinto(pos_actual, laberinto, camino, ANCHO, ALTO)
        
    escritor_solucion(solucion, ANCHO, ALTO) #crea un archivo con la solución


principal()
