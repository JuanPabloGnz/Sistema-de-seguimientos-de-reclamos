class MonticuloMediana:
    """
    Clase que implementa un monticulo de mediana, el cual permite calcular la mediana de una lista de numeros.
    Utiliza dos monticulos binarios, uno para los valores menores o iguales a la mediana y otro para los valores mayores a la mediana."""
    def __init__(self):
        '''Inicializa el monticulo de mediana con dos monticulos binarios, uno para los valores menores o iguales a la mediana y otro para los valores mayores a la mediana.
        La mediana se inicializa como None.'''
        self.__mediana = None
        self.__monticulo_min = MonticuloBinario("min")
        self.__monticulo_max = MonticuloBinario("max")

    @property
    def mediana(self):
        """Devuelve la mediana actual del montículo."""
        return self.__mediana
    
    @property
    def monticulo_min(self):
        """Devuelve el montículo de valores mayores o iguales a la mediana."""
        return self.__monticulo_min
    
    @property
    def monticulo_max(self):
        """Devuelve el montículo de valores menores o iguales a la mediana."""
        return self.__monticulo_max
    
    def construir_monticulo(self,p_lista):
        """Construye el monticulo de mediana a partir de una lista de numeros enteros positivos.
        Si la lista está vacía, la mediana se establece como None."""
        if len(p_lista) > 0:
            for n in p_lista:
                self.agregar_valor(n)
                self.__definir_mediana()
        else:
            self.__mediana = None
            
    def agregar_valor(self,p_valor):
        """Agrega un valor al monticulo de mediana y actualiza la mediana."""
        if not isinstance(p_valor,(int,float)):
            raise TypeError("El valor a agregar debe ser un número entero o decimal")
        if self.__mediana == None:
            self.__monticulo_min.insertar(p_valor)
        elif p_valor >= self.__mediana:
            if self.__monticulo_min.tamanoActual - self.__monticulo_max.tamanoActual <= 0:
                self.__monticulo_min.insertar(p_valor)
            else: #Reequilibrar el monticulo
                temp = self.__monticulo_min.listaMonticulo[1]
                self.__monticulo_min.eliminar()
                self.__monticulo_max.insertar(temp)  
                self.__monticulo_min.insertar(p_valor)
        else:
            if self.__monticulo_max.tamanoActual - self.__monticulo_min.tamanoActual <= 0:
                self.__monticulo_max.insertar(p_valor)
            else: #Reequilibrar el monticulo
                temp = self.__monticulo_max.listaMonticulo[1]
                self.__monticulo_max.eliminar()
                self.__monticulo_min.insertar(temp)
                self.__monticulo_max.insertar(p_valor)

    def __definir_mediana(self):
        """Define la mediana del monticulo de mediana en base a los monticulos maximo y minimo.""" 
        if len(self.__monticulo_max.listaMonticulo) > len(self.__monticulo_min.listaMonticulo):
            self.__mediana = self.__monticulo_max.listaMonticulo[1]
        elif len(self.__monticulo_max.listaMonticulo) == len(self.__monticulo_min.listaMonticulo):
            self.__mediana = (self.__monticulo_max.listaMonticulo[1] + self.__monticulo_min.listaMonticulo[1]) / 2
        else:
            self.__mediana = self.__monticulo_min.listaMonticulo[1] 
   
    def devolver_tamaño(self):
        """Devuelve el tamaño total del monticulo de mediana, que es la suma de los tamaños de los monticulos maximo y minimo.""" 
        return (self.__monticulo_min.tamanoActual + self.__monticulo_max.tamanoActual)
    

class MonticuloBinario:
    """Clase que implementa un monticulo binario, el cual puede ser de tipo minimo o maximo.
    Permite insertar eliminar valores, y construir un monticulo a partir de una lista de numeros enteros positivos.
    El monticulo se representa como una lista, donde el primer elemento es un 0 para facilitar el manejo de índices."""    
    def __init__(self, p_tipo):
        self.listaMonticulo = [0]
        self.tamanoActual = 0
        self.esMin = True
        if p_tipo != "min":
           self.esMin = False
    
    

    def infiltArriba(self,i):
        """Infiltro un elemento hacia arriba en el monticulo, para mantener la propiedad del monticulo.
        El elemento se infiltro desde la posición i hasta la raíz del monticulo."""
        #Monticulo de minimo
        if self.esMin == True:
            while i // 2 > 0:
                if self.listaMonticulo[i] < self.listaMonticulo[i // 2]:
                    tmp = self.listaMonticulo[i // 2]
                    self.listaMonticulo[i // 2] = self.listaMonticulo[i]
                    self.listaMonticulo[i] = tmp
                i = i // 2
        #Monticulo de maximo
        else:
            while i // 2 > 0:
                if self.listaMonticulo[i] > self.listaMonticulo[i // 2]:
                    tmp = self.listaMonticulo[i // 2]
                    self.listaMonticulo[i // 2] = self.listaMonticulo[i]
                    self.listaMonticulo[i] = tmp
                i = i // 2
                
    def insertar(self,k):
        """Inserta un valor en el montiuclo y lo infiltro hacia arriba para mantener la propiedad del monticulo.
        El valor se agrega al final de la lista y luego se infiltro hacia arriba desde la última posición."""
        self.listaMonticulo.append(k)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArriba(self.tamanoActual)

    def infiltAbajo(self,i):
        '''Infiltro un elemento hacia abajo en el monticulo, para mantener la propiedad del monticulo.
        El elemento se infiltro desde la posición i hasta las hojas del monticulo.'''  
        #Monticulo de minimo
        if self.esMin == True:
            while (i * 2) <= self.tamanoActual:
                hm = self.hijo(i)
                if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                    tmp = self.listaMonticulo[i]
                    self.listaMonticulo[i] = self.listaMonticulo[hm]
                    self.listaMonticulo[hm] = tmp
                i = hm
        #Monticulo de maximos
            else:
                while (i * 2) <= self.tamanoActual:
                    hm = self.hijo(i)
                    if self.listaMonticulo[i] < self.listaMonticulo[hm]:
                        tmp = self.listaMonticulo[i]
                        self.listaMonticulo[i] = self.listaMonticulo[hm]
                        self.listaMonticulo[hm] = tmp
                    i = hm
                
    def hijo(self,i):
        """
        Define cual de los hijos va a ser intercambiado por el ancestro
        """
        #Hijo minimo
        if self.esMin == True:
            if i * 2 + 1 > self.tamanoActual:
                return i * 2
            else:
                if self.listaMonticulo[i*2] < self.listaMonticulo[i*2+1]:
                    return i * 2
                else:
                    return i * 2 + 1
        #Hijo maximo
        else:
            if i * 2 + 1 > self.tamanoActual:
                return i * 2
            else:
                if self.listaMonticulo[i*2] > self.listaMonticulo[i*2+1]:
                    return i * 2
                else:
                    return i * 2 + 1
    def eliminar(self):
        '''Elimina el valor de la raíz del monticulo y lo infiltro hacia abajo para mantener la propiedad del monticulo.
        El valor eliminado es el primer elemento de la lista, que es la raíz del monticulo.
        Se reemplaza la raíz por el último elemento del monticulo y se infiltro hacia abajo desde la raíz.'''
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado

    def construirMonticulo(self,unaLista):
        '''Construye el monticulo a partir de una lista de numeros enteros positivos.
        La lista se copia a la lista del monticulo, y luego se infiltro hacia abajo desde la mitad de la lista hasta la raíz.
        Esto asegura que todos los elementos del monticulo cumplan con la propiedad del monticulo.'''
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while (i > 0):
            self.infiltAbajo(i)
            i = i - 1


if __name__ == "__main__":
    # lista = [1,7,4,8,1,7,5,9]

    # lista = [1,2,3,4,5,6,7,8,9]

    # lista = [9,8,7,6,5,4,3,2,1]
    
    # lista = [1,0,0,0,0,0]
    
    lista = [7, 1, 5, 2, 6, 8]
    monticulomed = MonticuloMediana()

    monticulomed.construir_monticulo(lista)

    print("La lista a trabajar es:", lista)
    print(monticulomed.mediana)

    print("monticulo izquierdo:",monticulomed.monticulo_max.listaMonticulo)
    print("monticulo derechho", monticulomed.monticulo_min.listaMonticulo)
