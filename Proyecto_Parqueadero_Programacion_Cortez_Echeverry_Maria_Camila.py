import json

with open ('usuarios.json', 'r', encoding = 'utf-8') as file:
    lusuarios = json.load(file)
with open ('tiposParqueaderos.json', 'r') as file2:
    parqueaderos = json.load(file2)

def retiro(lusuarios, parqueaderos):  ##Datos necesarios para retirar
	pl = input("Ingrese su placa: ")
	hora = eval(input("Ingrese el numero de horas que ha permanecido en el parqueadero: "))
	lis =[]
	fila = 0
	columna = 0
	piso = 0
	for x in parqueaderos:
		for w in parqueaderos[x]:
			piso += 1
			for y in w:
				fila += 1
				if type(y) == list:
					columna += 1
					if pl in y[1]:
						for verificar in lusuarios["usuarios"]:
							lis.append(verificar[3])	
						if pl in lis:
							for i in lusuarios["usuarios"]:
								if pl == i[3]:
									tipo, plan, tv = i[2], i[5], i[4]
						else:
							plan = ("Diario")
							tv = y[0]
							tipo = ("Visitante")
						cobro(plan, tipo, hora)
						nPiso = NumeroDePiso(piso)
						UpdateLista = liberarParq(tv, fila, columna, nPiso, parqueaderos)
						parqueaderos.update({piso: UpdateLista})
						with open('tiposParqueaderos.json', 'w') as jsonFile3:
							json.dump(parqueaderos, jsonFile3, ensure_ascii=False)
							jsonFile3.close
						print("Vuelva Pronto")

def cobro(plan, tipo, hora): #Realiza el cobro correspondiente ##Esta es a la funcion que solo sirve con debug
	if plan == "Diario":
		if tipo == "Estudiante":
			cobro = hora * 1000
		elif tipo == "Profesor":
			cobro = hora * 2000
		elif tipo == "Personal Administrativo":
			cobro = hora * 1500
		else:
			cobro = hora * 3000
		print("El total a pagar es de $" + str(cobro))
	else:
		print("No debe realizar ningún pago")		
	
def liberarParq(tv, fila, columna, nPiso, parqueaderos): #Quita el tipo de vehiculo y la placa del parqueadero
	nv = asignarnumero(tv)
	i = parqueaderos[nPiso]
	i[(fila - 1)].pop((columna - 1))
	i[(fila - 1)].insert((columna - 1), nv)
	return i
	
def ingresar(lusuarios, parqueaderos): ##Verifica si el usuario esta registrado.
	pl = input("Ingrese la placa de su vehiculo: ")
	tipo, plan = "", ""
	lis, lisv, lispark = [], [], []
	for verificar in lusuarios["usuarios"]:
		lis.append(verificar[3])
	if pl in lis:
		for i in lusuarios["usuarios"]:
			if pl == i[3]:
				tipo, plan, tv = i[2], i[5], i[4]
				lispark.append(tv)
				lispark.append(pl)
				numerov = asignarnumero(tv)
				for x in parqueaderos:##Que recorra las llaves
					for w in parqueaderos[x]:
						for ii in w:
							lisv.append(ii)
				if numerov in lisv:##Si hay parqueadero para su tipo de vehiculo
					CuposVacios(parqueaderos, numerov)
					piso = input("Seleccione el piso: \n 1. Piso 1 \n 2. Piso 2 \n 3. Piso 3 \n 4. Piso 4  \n 5. Piso 5 \n 6. Piso 6 \n ")
					nupi = NumeroDePiso(piso)
					print(parqOcupado(parqueaderos, numerov, nupi))
					# respuesta = str(input("¿Desea escoger otro piso? \n 1. Si \n 2. No \n"))
					seleccionHorizontal = int(input("Ingrese la fila: "))
					seleccionVertical = int(input("Ingrese la columna: "))
					validarSelec = validaSeleccionUsuario(seleccionHorizontal, seleccionVertical, numerov, parqueaderos, nupi)
					while validarSelec != True:
						print("|--------Por favor seleccione un espacio disponible o que no exceda el tamaño--------|")
						seleccionHorizontal = int(input("Ingrese la fila: "))
						seleccionVertical = int(input("Ingrese la columna: "))
						validarSelec = validaSeleccionUsuario(seleccionHorizontal, seleccionVertical, numerov, parqueaderos, nupi)
					UpdateLista = insertarDatosEnMatriz(seleccionHorizontal, seleccionVertical, nupi, lispark, parqueaderos)
					parqueaderos.update({nupi: UpdateLista})
					with open('tiposParqueaderos.json', 'w') as jsonFile2:
						json.dump(parqueaderos, jsonFile2, ensure_ascii=False)
						jsonFile2.close
					print("Adelante")
	elif pl not in lis:
		tipo = "Visitante"
		print(tipo)
		plan = "Diario"
		print(plan)
		tv = input("Ingrese  su tipo de vehiculo: \n 1. Automóvil \n 2. Automóvil Eléctrico \n 3. Motocicleta \n 4. Discapacitado \n")
		lispark.append(tv)
		lispark.append(pl)
		numerov = asignarnumero(tv)
		for x in parqueaderos:          ##Que recorra las llaves
			for w in parqueaderos[x]:
				for ii in w:
					lisv.append(ii)
		if numerov in lisv:  ##Si hay parqueadero para su tipo de vehiculo
				CuposVacios(parqueaderos, numerov)
				piso = input("Seleccione el piso: \n 1. Piso 1 \n 2. Piso 2 \n 3. Piso 3 \n 4. Piso 4  \n 5. Piso 5 \n 6. Piso 6 \n ")
				nupi = NumeroDePiso(piso)
				print(parqOcupado(parqueaderos, numerov, nupi))
				# respuesta = str(input("¿Desea escoger otro piso? \n 1. Si \n 2. No \n"))
				seleccionHorizontal = int(input("Ingrese la fila: "))
				seleccionVertical = int(input("Ingrese la columna: "))
				validarSelec = validaSeleccionUsuario(seleccionHorizontal, seleccionVertical, numerov, parqueaderos, nupi)
				while validarSelec != True:
					print("|--------Por favor seleccione un espacio disponible o que no exceda el tamaño--------|")
					seleccionHorizontal = int(input("Ingrese la fila: "))
					seleccionVertical = int(input("Ingrese la columna: "))
					validarSelec = validaSeleccionUsuario(seleccionHorizontal, seleccionVertical, numerov, parqueaderos, nupi)
				UpdateLista = insertarDatosEnMatriz(seleccionHorizontal, seleccionVertical, nupi, lispark, parqueaderos)
				parqueaderos.update({nupi: UpdateLista})
				with open('tiposParqueaderos.json', 'w') as jsonFile2:
					json.dump(parqueaderos, jsonFile2, ensure_ascii=False)
					jsonFile2.close
				print("Adelante")
	return plan

def validaSeleccionUsuario(fila, col, veh, parqueaderos, piso): ##Valida si el usuario escogio un parqueadero disponible o dentro del rango
	i = parqueaderos[piso]
	if fila > len(i):
		return False
	if col > len(i):
		return False
	if veh == 2:
		if i[(fila - 1)][col - 1] == 2 or i[(fila - 1)][col - 1] == 1:
			return True
	elif veh == 4:
		if i[(fila - 1)][col - 1] == 4 or i[(fila - 1)][col - 1] == 1:
			return True
	else:
		if i[(fila - 1)][col - 1] == veh:
			return True
	return False

def insertarDatosEnMatriz(fila, columna, piso, carro, parqueaderos): ##Cambia el numero del parqueadero por el tipo de ususraio y la placa
	i = parqueaderos[piso]
	i[(fila - 1)].pop((columna - 1))
	i[(fila - 1)].insert((columna - 1), carro)
	return i	
	
def asignarnumero(tv):  ##Enumera al vehiculo segun su tipo
    nv = 0 
    if tv == '1' or tv == "Automóvil":
        nv = 1
    elif tv == '2' or tv == "Automóvil Eléctrico":
        nv = 2
    elif tv == '3' or  tv == "Motocicleta":
        nv = 3
    elif tv == '4' or  tv == "Discapacitado":
        nv = 4
    return nv

def NumeroDePiso(piso):  ##Escoge el numero de piso para luego ingresarlo en    nupi = NumeroDePiso(piso)
	n = " "
	if piso == '1' or piso == "Piso 1" or piso == 1:
		n = "Piso1"
	elif piso == '2' or piso == "Piso 2" or piso == 2:
		n = "Piso2"
	elif piso == '3' or piso == "Piso 3" or piso == 3:
		n = "Piso3"
	elif piso == '4' or piso == "Piso 4" or piso == 4:
		n = "Piso4"
	elif piso == '5' or piso == "Piso 5" or piso == 5:
		n = "Piso5"
	elif piso == '6' or piso == "Piso 6" or piso == 6:
		n = "Piso6"
	return n

def parqOcupado(parqueaderos, numerov, nupi): ##Imprime la grafica de los parqueaderos
	print("\n" + "Piso: " + nupi + " - Las X estan ocupados, los 0 estan disponibles")
	print(end = "\n")
	for i in parqueaderos[nupi]:
		lis = []
		for x in i:
			if numerov == 2:
				if x == numerov or x == 1:
					lis.append("0")
				else:
					lis.append("X")
			elif numerov == 4:
				if x == numerov or x == 1:
					lis.append("0")
				else:
					lis.append("X")
			else:
				if x == numerov:
					lis.append("0")
				else:
					lis.append("X")
		print(lis)
		print(end = "\n")

def CuposVacios(parqueaderos, numerov): ##Cuantos parqueaderos vacios hay por piso
	for k in parqueaderos:
		lisg = []
		contadorDeCuposVacios = 0
		for i in parqueaderos[k]:
			lis = []  
			for x in i:
				if numerov == 2:
					if x == numerov or x == 1:
						lis.append("0")
						contadorDeCuposVacios += 1
				elif numerov == 4:
					if x == numerov or x == 1:
						lis.append("0")
						contadorDeCuposVacios += 1
				else:
					if x == numerov:
						contadorDeCuposVacios += 1
		print("En el " + k + " es de " + str(contadorDeCuposVacios) + " Cupos vacios")

def registro(lusuarios): ##Funcion que registra a los usuarios
    nom = input("Ingrese su nombre: ")
    id = int(input("Ingrese su numero de identificacion: "))
    nUsuario, lis = [], [] #Lista para el nuevo usuario y lista donde se guarda el id del archivo 
    for x in lusuarios["usuarios"]: #Verifica si el id ingresado esta en la lista de ids registrados
        lis.append(x[1])
    if id in lis:
        respuesta = "Un usuario no puede registrar mas de un vehiculo"
        print(respuesta)
    else:
        tipo = input("Ingrese su tipo de usuario: ")
        placa = input("Ingrese la placa de su vehiculo: ")
        vehiculo = input("Ingrese el tipo de vehiculo (Usar tildes): ")
        plan = input("Ingrese su plan de pago: ")
        nUsuario.append(nom)
        nUsuario.append(id)
        nUsuario.append(tipo)
        nUsuario.append(placa)
        nUsuario.append(vehiculo)
        nUsuario.append(plan)
    lusuarios["usuarios"].append(nUsuario)
    with open('usuarios.json', 'w') as jsonFile:
        json.dump(lusuarios, jsonFile, ensure_ascii=False)
        jsonFile.close
    return nUsuario 

#MENU
print("      ------ MENU ------")
try:
	menu = int(input("| Ingrese la accion que desea realizar: \n| 1. Registrar el vehiculo \n| 2. Ingreso de vehiculo \n| 3. Retirar vehiculo \n| 4. Generar reporte \n| 5. Salir \n"))
	while menu != 5:
		if menu == 1:
			registro(lusuarios)
		elif menu == 2:
			ingresar(lusuarios, parqueaderos)
		elif menu == 3:
			retiro(lusuarios, parqueaderos)
		menu = int(input("| Ingrese la accion que desea realizar: \n| 1. Registrar el vehiculo \n| 2. Ingreso de vehiculo \n| 3. Retirar vehiculo \n| 4. Generar reporte \n| 5. Salir \n"))
except ValueError:
    print("Ingrese una accion valida")
