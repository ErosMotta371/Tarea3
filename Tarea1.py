import graphviz

class NodoA:
    def __init__(self, valor):
        self.izq = None
        self.der = None
        self.valor = valor

class ArbolBB:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self.insertar2(valor, self.raiz)

    def insertar2(self, valor, nodo):
        if nodo is None:
            return NodoA(valor)
        if valor < nodo.valor:
            nodo.izq = self.insertar2(valor, nodo.izq)
        elif valor > nodo.valor:
            nodo.der = self.insertar2(valor, nodo.der)
        return nodo

    def buscar(self, valor):
        return self.buscar2(valor, self.raiz)

    def buscar2(self, valor, nodo):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self.buscar2(valor, nodo.izq)
        else:
            return self.buscar2(valor, nodo.der)

    def eliminar(self, valor):
        self.raiz = self.eliminar2(self.raiz, valor)

    def eliminar2(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izq = self.eliminar2(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self.eliminar2(nodo.der, valor)
        else:
            if nodo.izq is None:
                temp = nodo.der
                nodo = None
                return temp
            elif nodo.der is None:
                temp = nodo.izq
                nodo = None
                return temp
            temp = self.min_valor_nodo(nodo.der)
            nodo.valor = temp.valor
            nodo.der = self.eliminar2(nodo.der, temp.valor)
        return nodo

    def min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual
    
    def mostrar(self, nodo, g):
        if nodo is not None:
            g.node(str(nodo.valor))
            if nodo.izq is not None:
                g.edge(str(nodo.valor), str(nodo.izq.valor))
                self.mostrar(nodo.izq,g)
            if nodo.der is not None:
                g.edge(str(nodo.valor), str(nodo.der.valor))
                self.mostrar(nodo.der,g)

def guardar_arbol_en_archivo(arbol, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        escribir_nodos_en_archivo(arbol.raiz, archivo)

def escribir_nodos_en_archivo(nodo, archivo):
    if nodo is not None:
        archivo.write(str(nodo.valor) + '\n')
        escribir_nodos_en_archivo(nodo.izq, archivo)
        escribir_nodos_en_archivo(nodo.der, archivo)

arch = "lectura.txt"
arbol = ArbolBB()
try:
    # Abrir el archivo en modo lectura
    with open(arch, 'r') as file_object:
        leer = file_object.readlines()
        contador = 0
    for l in leer:
        valor = l.strip()
        if valor.isdigit():
            arbol.insertar(int(valor))
            contador = contador + 1
        else:
            print(f"El valor '{valor}' en el archivo no es un número entero válido y será ignorado.")

    while(True):
        print("""Bienvenido al sistema de arboles binarios
        1. Insertar nodo al arbol binario
        2. Eliminar nodo del arbol binario
        3. Buscar nodo del arbol binario (recorrido)
        4. Mostrar arbol binario completo
        5. Salir""")
        Op = int(input("Ingrese una opcion del menu: "))

        if Op == 1:
            print("Usted ingreso la opcion de insertar un nodo en el arbol binario")
            x = int(input("Ingrese el numero para ingresar al arbol binario: "))
            arbol.insertar(x)
            # Guardar el árbol modificado en el archivo
            guardar_arbol_en_archivo(arbol, arch)
        elif Op == 2:
            print("Usted ingreso la opcion de eliminar un nodo en el arbol binario")
            x = int(input("Ingrese el numero para eliminar al arbol binario: "))
            arbol.eliminar(x)
            guardar_arbol_en_archivo(arbol, arch)
        elif Op == 3:
            print("Usted ingreso la opcion de buscar un nodo en el arbol binario")
            x = int(input("Ingrese el numero para buscar al arbol binario: "))
            resultado = arbol.buscar(x)
            if resultado:
                print(f"Valor {x} encontrado en el árbol.")
            else:
                print(f"Valor {x} no encontrado en el árbol.")
        elif Op == 4:
            print("Se esta imprimiendo el arbol binario")
            g = graphviz.Digraph('G', filename='arbol_binario.gv')
            arbol.mostrar(arbol.raiz, g)
            g.view()
        elif Op == 5:
            print("Saliendo del programa")
            break
        else:
            print("Ingrese una opción correcta")

except FileNotFoundError:
    print(f'El archivo "{arch}" no existe. Se creará el archivo.')

    with open(arch, 'w') as file_object:
        pass
