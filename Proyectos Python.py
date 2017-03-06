from flask import Flask, request
import os

app = Flask(__name__)

#------------------------------------------INICIO de MAtriz------------------------------------------------

class NodoMatriz():
    def __init__(self, x, y, correo):
        self.x = x
        self.y = y
        self.correo = correo
        self.up=None
        self.dw = None
        self.lf =None
        self.rg=None

#Estructura para la lista de filas
class Fila():
	def __init__(self):
		self.ini= None
		self.fin =None

	def insertarFrente(self, nuevo):
		self.ini.lf = nuevo
		nuevo.rg = self.ini
		self.ini=self.ini.lf

	def insertarMedio(self, nuevo):
		aux1=self.ini
		aux2=None

		while aux1.x < nuevo.x:
			aux1=aux1.rg

		aux2=aux1.lf

		if aux1.x == nuevo.x:
			return

		aux2.rg=nuevo
		aux1.lf = nuevo
		nuevo.rg = aux1
		nuevo.lf = aux2

	def insertarFin(self, nuevo):
		self.fin.rg = nuevo;
		nuevo.lf = self.fin
		self.fin= self.fin.rg

	def agregarNodoMatriz(self, nuevo):
		if self.ini == None:
			self.ini=nuevo
			self.fin =nuevo
		else:
			if nuevo.x < self.ini.x:
				self.insertarFrente(nuevo)
			elif nuevo.x > self.fin.x:
				self.insertarFin(nuevo)
			else:
				self.insertarMedio(nuevo)

#Estructura para la lista de columnas
class Columna():
	def __init__(self):
		self.ini= None
		self.fin =None

	def insertarFrente(self, nuevo):
		self.ini.up = nuevo
		nuevo.dw = self.ini
		self.ini=self.ini.up

	def insertarMedio(self, nuevo):
		aux1=self.ini
		aux2=None

		while aux1.y < nuevo.y:
			aux1=aux1.dw

		aux2=aux1.up

		if aux1.y == nuevo.y:
			return

		aux2.dw=nuevo
		aux1.up = nuevo
		nuevo.dw = aux1
		nuevo.up = aux2

	def insertarFin(self, nuevo):
		self.fin.dw = nuevo;
		nuevo.up = self.fin
		self.fin= self.fin.dw

	def agregarNodoMatriz(self, nuevo):
		if self.ini == None:
			self.ini=nuevo
			self.fin =nuevo
		else:
			if nuevo.y < self.ini.y:
				self.insertarFrente(nuevo)
			elif nuevo.y > self.fin.y:
				self.insertarFin(nuevo)
			else:
				self.insertarMedio(nuevo)

#Estructura para los nodos guias de las columnas
class CabezaColumna():
	def __init__(self,x):
		self.sig= None
		self.ant =None
		self.x=x
		self.col= Columna()

#Estructura para los nodos guias de las filas
class CabezaFila():
	def __init__(self,y):
		self.sig= None
		self.ant =None
		self.y=y
		self.fil= Fila()

#Estructura para la lista de CabezaColumna
class Cabeceras():
	def __init__(self):
		self.ini= None
		self.fin =None

	def insertarFrente(self, nuevo):
		self.ini.ant = nuevo
		nuevo.sig = self.ini
		self.ini=nuevo

	def insertarMedio(self, nuevo):
		aux1=self.ini
		aux2=None

		while aux1.x < nuevo.x:
			aux1=aux1.sig

		aux2=aux1.ant

		aux2.sig=nuevo
		aux1.ant=nuevo
		nuevo.sig=aux1
		nuevo.ant=aux2

	def insertarFin(self, nuevo):
		self.fin.sig = nuevo
		nuevo.ant = self.fin
		self.fin = self.fin.sig

	def agergarCabezaCol(self, nuevo):
		if self.ini==None:
			self.ini=nuevo
			self.fin = nuevo
			print("se estabecio como ini y fin")
		else:
			if nuevo.x < self.ini.x:

				self.insertarFrente(nuevo)
				print(self.ini.__dict__)
				print("inserto frente y el siguiente es " + self.ini.sig.x)
			elif nuevo.x > self.fin.x:
				print("inserto fin")
				print("vaa a insertar fin")
				self.insertarFin(nuevo)
			else:
				print("inserto medio")
				self.insertarMedio(nuevo)




	def existe(self, x):
		if self.ini == None:
			print("retorno falso")
			return False
		else:
			temp=self.ini
			while temp!=None:
				if temp.x==x:
					print("retorno verdad")
					return True
				elif temp.sig==None:
					print("retorno falso2")
					return False

				temp = temp.sig

	def busqueda(self, x):
		if self.existe(x):
			temp=self.ini
			while temp.x!=x:
				temp = temp.sig

			return temp
		else:
			nuevo = CabezaColumna("x")
			return nuevo

#Estructura para la lista de CabezaFila
class Laterales():
	def __init__(self):
		self.ini= None
		self.fin =None

	def insertarFrente(self, nuevo):
		self.ini.ant = nuevo
		nuevo.sig = self.ini
		self.ini=self.ini.ant

	def insertarMedio(self, nuevo):
		aux1=self.ini
		aux2=""

		while aux1.x < nuevo.x:
			aux1=aux1.sig

		aux2=aux1.ant

		aux2.sig=nuevo
		aux1.ant=nuevo
		nuevo.sig=aux1
		nuevo.ant=aux2

	def insertarFin(self, nuevo):
		self.fin.sig = nuevo
		nuevo.ant = self.fin
		self.fin = self.fin.sig

	def agergarCabezaFil(self, nuevo):
		if self.ini==None:
			self.ini=nuevo
			self.fin = nuevo
		else:
			if nuevo.y < self.ini.y:
				self.insertarFrente(nuevo)
			elif nuevo.y > self.fin.y:
				self.insertarFin(nuevo)
			else:
				self.insertarMedio(nuevo)

	def existe(self, y):
		if self.ini == None:
			return False
		else:
			temp=self.ini
			while temp!=None:
				if temp.y==y:
					return True
				elif temp.sig==None:
					return False

				temp = temp.sig

	def busqueda(self, y):
		if self.existe(y):
			temp=self.ini
			while temp.y!=y:
				temp = temp.sig

			return temp
		else:
			nuevo = CabezaFila("z")
			return nuevo

#Nodo guia de la matriz
class Matriz():
	def __init__(self):
		self.listaX= Cabeceras()
		self.listaY =Laterales()

	def agregarNodoMatriz(self,x,y,email):
		nuevo = NodoMatriz(x,y,email)
		if self.listaX.existe(x)==False:
			nuevaC = CabezaColumna(x)
			self.listaX.agergarCabezaCol(nuevaC)
		if self.listaY.existe(y)==False:
			nuevaF = CabezaFila(y)
			self.listaY.agergarCabezaFil(nuevaF)

		auxCol = self.listaX.busqueda(x)
		auxFil = self.listaY.busqueda(y)

		auxCol.col.agregarNodoMatriz(nuevo)
		auxFil.fil.agregarNodoMatriz(nuevo)

	def buscarX(self,x):
		if self.listaX.existe(x):
			return True
		else:
			return False

	def buscarY(self, y):
		if self.listaY.existe(y):
			return True
		else:
			return False

	def imprimirMatriz(self):

		tempC = self.listaX.ini
		tempF = self.listaY.ini
		outfile = open('C:\\Users\\KMMG\\Desktop\\matriz.dot', 'w')
		outfile.write('digraph G{\n')
		outfile.write('I[label=\"Matriz\", style=filled]\n')
		dom = tempC.x.replace(".","")
		outfile.write('{rank=same; c'+dom+' I }\n')
		outfile.write('I -> c'+dom+'\n')
		outfile.write('I -> l' + tempF.y + '\n')

		tempC = self.listaX.ini
		tempF = self.listaY.ini



		while tempC!=None:
			dom = tempC.x.replace(".", "")
			outfile.write('c'+dom+'[label=\"'+tempC.x+'\", style=filled, shape=box]\n')
			if tempC.sig!=None:
				doms = tempC.sig.x.replace(".", "")
				outfile.write('{rank=same; c'+dom+' c'+doms+'}\n')
				outfile.write(' c'+dom+' -> c'+doms+'\n')
				outfile.write(' c' + doms+ ' -> c' + dom + '\n')

			tempC = tempC.sig

		while tempF!=None:
			outfile.write('l'+tempF.y+'[label=\"'+tempF.y+'\", style=filled, shape=box]\n')
			if tempF.sig!=None:
				#outfile.write('{rank=same; l'+tempF.y+' l'+tempF.sig.y+'}\n')
				outfile.write('l'+tempF.y+' -> l'+tempF.sig.y+'\n')
				outfile.write('l' + tempF.sig.y + ' -> l' + tempF.y + '\n')

			tempF = tempF.sig

		tempC = self.listaX.ini

		while tempC!=None:
			nodoM= tempC.col.ini
			dom = tempC.x.replace(".","")
			outfile.write('subgraph s'+dom+'{\n')
			while nodoM != None:
				ddn = nodoM.x.replace(".","")
				outfile.write('c' + ddn + 'l'+nodoM.y+'[label=\"'+nodoM.correo+'\", style=filled, shape=box]\n')
				nodoM = nodoM.dw
			outfile.write('}\n')
			tempC =tempC.sig

		tempC = self.listaX.ini

		while tempC !=None:
			nodoM = tempC.col.ini
			while nodoM !=None:
				ddn = nodoM.x.replace(".","")
				if nodoM.rg != None:
					drn = nodoM.rg.x.replace(".","")
					outfile.write('c' + ddn + 'l'+nodoM.y + ' -> c' + drn + 'l'+nodoM.rg.y+'\n')
					outfile.write('{rank=same; c' + ddn + 'l'+nodoM.y + '  c' + drn + 'l'+nodoM.rg.y+'}\n')
				if nodoM.dw != None:
					ddw = nodoM.dw.x.replace(".", "")
					outfile.write('c' + ddn + 'l'+nodoM.y + ' -> c' + ddw + 'l'+nodoM.dw.y+'\n')
				if nodoM.up != None:
					dun = nodoM.up.x.replace(".", "")
					outfile.write('c' + ddn + 'l'+nodoM.y + ' -> c' + dun + 'l'+nodoM.up.y+'\n')
				if nodoM.lf != None:
					dln = nodoM.lf.x.replace(".", "")
					outfile.write('c' + ddn + 'l'+nodoM.y + ' -> c' + dln + 'l'+nodoM.lf.y+'\n')
					outfile.write('{rank=same; c' + ddn + 'l'+nodoM.y + '  c' + dln + 'l'+nodoM.lf.y+'}\n')
				nodoM = nodoM.dw
			tempC = tempC.sig

		tempC = self.listaX.ini
		tempF = self.listaY.ini

		while tempF != None:
			nodoM = tempF.fil.ini
			ddn = nodoM.x.replace(".","")
			if tempF.fil.ini != None:
				outfile.write('l'+tempF.y+' -> c' + ddn + 'l'+nodoM.y + '\n')
				outfile.write('{rank=same; l'+tempF.y+'  c' + ddn + 'l' + nodoM.y + '}\n')
			tempF = tempF.sig

		while tempC != None:
			nodoM = tempC.col.ini
			dom = tempC.x.replace(".", "")
			ddn = nodoM.x.replace(".", "")
			if tempC.col.ini!=None:
				outfile.write('c'+dom+' -> c' + ddn + 'l'+nodoM.y + '\n')
			tempC = tempC.sig
		outfile.write('}')
		outfile.close()

		os.system("dot -Tpng C:\\Users\\KMMG\\Desktop\\matriz.dot -o C:\\Users\\KMMG\\Desktop\\matriz.png")



#------------------------------------------FIN DE MATRIZ---------------------------------------

#Nodo para pila y cola
class Nodo():
	def __init__(self,num):
		self.num=num
		self.sig=None

#------------------------------------------Inicio COLA-------------------------------------------

class Cola():
	def __init__(self):
		self.inicio = None

	def queue(self, num):
		nuevo=Nodo(num)
		if self.inicio==None:
			self.inicio=nuevo
		else:
			temp = self.inicio
			while temp.sig!=None:
				temp=temp.sig
			temp.sig=nuevo

	def dequeue(self):
		if self.inicio==None:
			return "a"
		else:
			regreso = self.inicio.num
			self.inicio=self.inicio.sig
			return regreso
	def imprimirCola(self):
		outfile = open('C:\\Users\\KMMG\\Desktop\\cola.dot', 'w')
		outfile.write('digraph G{\n')
		temp = self.inicio
		while temp!=None:
			outfile.write(temp.num+'[label=\"'+temp.num+'\", style=filled, shape=box]\n')
			if temp.sig!=None:
				outfile.write(temp.num+' -> '+temp.sig.num+'\n')
			temp= temp.sig

		outfile.write('}')
		outfile.close()

		os.system("dot -Tpng C:\\Users\\KMMG\\Desktop\\cola.dot -o C:\\Users\\KMMG\\Desktop\\cola.png")

#------------------------------------------Fin COLA-------------------------------------------

#------------------------------------------Inicio PILA-------------------------------------------

class Pila():
	def __init__(self):
		self.inicio = None

	def push(self, num):
		nuevo=Nodo(num)
		if self.inicio==None:
			self.inicio=nuevo
		else:
			nuevo.sig=self.inicio
			self.inicio=nuevo

	def pop(self):
		if self.inicio==None:
			return "a"
		else:
			regreso = self.inicio.num
			self.inicio=self.inicio.sig
			return regreso
	def imprimirPila(self):
		outfile = open('C:\\Users\\KMMG\\Desktop\\pila.dot', 'w')
		outfile.write('digraph G{\n')
		temp = self.inicio
		while temp!=None:
			outfile.write(temp.num+'[label=\"'+temp.num+'\", style=filled, shape=box]\n')
			if temp.sig!=None:
				outfile.write(temp.num+' -> '+temp.sig.num+'\n')
			temp= temp.sig

		outfile.write('}')
		outfile.close()

		os.system("dot -Tpng C:\\Users\\KMMG\\Desktop\\pila.dot -o C:\\Users\\KMMG\\Desktop\\pila.png")



#------------------------------------------------fin COLA--------------------------------------------

#nodo para la lista
class NodoLista():
	def __init__(self,contenido,indice):
		self.contenido=contenido
		self.indice=indice
		self.sig=None

class Lista():
	def __init__(self):
		self.inicio=None
		self.fin=None

	def agergar(self,conte):
		indice=0
		if self.inicio!=None:
			temp = self.inicio
			while temp!=None:
				indice+=1
				temp = temp.sig

		nuevo = NodoLista(conte,indice)

		if self.inicio==None:
			self.inicio=nuevo
			self.fin=nuevo
		else:
			temp= self.inicio
			while temp.sig!=None:
				temp = temp.sig
			temp.sig = nuevo
			self.fin=nuevo

	def buscar(self,conte):
		temp = self.inicio
		while temp!=None:
			if temp.contenido==conte:
				return temp.indice
			temp = temp.sig;
		return "a"

	def buscarIndice(self,indice):
		temp = self.inicio
		while temp!=None:
			if temp.indice==indice:
				return True
			temp = temp.sig;
		return False

	def reorganiza(self):
		temp = self.inicio
		i=0
		while temp!=None:
			temp.indice=i
			i+=1
			temp=temp.sig

	def eliminar(self, indi):
		busq = self.buscarIndice(indi)
		if busq==True:
			if indi==self.inicio.indice:
				self.inicio=self.inicio.sig
			elif indi==self.fin.indice:
				temp = self.inicio
				while temp.sig!=self.fin:
					temp=temp.sig
				temp.sig=None
				self.fin=temp
			else:
				temp = self.inicio
				while temp.sig.indice != indi:
					temp = temp.sig
				temp.sig = temp.sig.sig
			self.reorganiza()
			return "Elemento eliminado"
		else:
			return "No existe en la lista"

	def imprimirLista(self):
		outfile = open('C:\\Users\\KMMG\\Desktop\\lista.dot', 'w')
		outfile.write('digraph G{\n')
		temp = self.inicio
		while temp != None:
			outfile.write(str(temp.indice) + '[label=\"Indice: ' + str(temp.indice) + '\\n Palabra: '+temp.contenido+'\", style=filled, shape=box]\n')
			if temp.sig != None:
				outfile.write(str(temp.indice) + ' -> ' + str(temp.sig.indice) + '\n')
				outfile.write('{rank=same; '+str(temp.indice) + ' ' + str(temp.sig.indice)+ '}\n')
			temp = temp.sig

		outfile.write('}')
		outfile.close()

		os.system("dot -Tpng C:\\Users\\KMMG\\Desktop\\lista.dot -o C:\\Users\\KMMG\\Desktop\\lista.png")







ematriz = Matriz()
ecola = Cola()
epila = Pila()
elista = Lista()

@app.route("/agergarCorreo", methods=['POST'])
def agregarCorreo():
	dominio = str(request.form['dominio'])
	letra = str(request.form['letra'])
	correo = str(request.form['correo'])
	ematriz.agregarNodoMatriz(dominio, letra, correo)
	ematriz.imprimirMatriz()
	return "Correo Agregado"

@app.route("/buscarDominio", methods=['POST'])
def buscarDominio():
	dominio = str(request.form['dominio'])
	respuesta =""
	if ematriz.buscarX(dominio):
		auxCol = ematriz.listaX.busqueda(dominio)
		auxIni = auxCol.col.ini
		while auxIni!=None:
			respuesta+=auxIni.correo+" "
			auxIni= auxIni.dw
	else:
		respuesta="No existen con ese dominio"

	return respuesta

@app.route("/buscarLetra", methods=['POST'])
def buscarLetra():
	letra = str(request.form['letra'])
	respuesta =""
	if ematriz.buscarY(letra):
		auxFil = ematriz.listaY.busqueda(letra)
		auxIni = auxFil.fil.ini
		while auxIni!=None:
			respuesta+=auxIni.correo+" "
			auxIni= auxIni.rg
	else:
		respuesta="No existen con ese dominio"

	return respuesta

@app.route("/queue", methods=['POST'])
def queue():
	num = str(request.form['num'])
	ecola.queue(num)
	ecola.imprimirCola()

	return "Agregado a la Cola"

@app.route("/dequeue", methods=['POST'])
def dequeue():
	a = str(request.form['a'])
	res = ecola.dequeue()
	ecola.imprimirCola()
	if res == "a":
		res="Cola Vacia"

	print (res)
	return res

@app.route("/push", methods=['POST'])
def push():
	num = str(request.form['num'])
	epila.push(num)
	epila.imprimirPila()

	return "Agregado a la Pila"

@app.route("/pop", methods=['POST'])
def pop():
	a = str(request.form['a'])
	res = epila.pop()
	epila.imprimirPila()
	if res == "a":
		res="Pila Vacia"

	print (res)
	return res

@app.route("/agregarLista", methods=['POST'])
def agregarLista():
	contenido = str(request.form['contenido'])
	elista.agergar(contenido)
	elista.imprimirLista()

	return "Agregado a la Lista"

@app.route("/buscarLista", methods=['POST'])
def buscarLista():
	contenido = str(request.form['contenido'])
	respuesta = elista.buscar(contenido)

	if respuesta == "a":
		respuesta="No se encontró el dato"
	else:
		respuesta = "Dato está en el indice "+str(respuesta)

	return respuesta


@app.route("/eliminarLista", methods=['POST'])
def eliminarLista():
	indi = str(request.form['indice'])
	indice = int(indi)
	respuesta = elista.eliminar(indice)
	elista.imprimirLista()


	return respuesta



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
