#Script para extraer los datos de jugadores registrados en FIFA
#Entrada: Se ejecuta sin entrada
#Salida: Se registran por lotes los datos de los jugadores en la base de datos Fifa2021


#conexión a la bd
import psycopg2
from psycopg2 import extras
from config import config
import time


import requests



def get_datos_juadores(datos_jugador):
	jugadores = []
	for jugador in datos_jugador:
		nombre = jugador['firstName'] + ' ' +jugador['lastName']
		posicion_juego = jugador['positionFull']
		nacionalidad = jugador['nation']['name']
		equipo = jugador['club']['name']
		jugadores.append((nombre,posicion_juego,nacionalidad,equipo))

	return jugadores


def conectar_BD():
	try :
		#Se extraen los parámetros de configuración de la base de datos
		params = config()
		# Se establece la conexión con la base de datos
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)#(host= 'localhost', dbname= 'Fifa2021', user= 'postgres', password= 'postgres',port="5432")

		# url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
		# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname) 
		# schema = "schema.sql" 
		# conn = psycopg2.connect(db) 
		# cur = conn.cursor()

		# Se crea el cursor
		cur = conn.cursor()

		
		#Al conectar a la base de datos verifica si existe la tabla y la borra
		sql = '''DROP TABLE IF EXISTS jugador'''
		cur.execute(sql)
		conn.commit()
		#Crea la tabla desde 0
		sql = '''CREATE TABLE IF NOT EXISTS jugador(
                    nombre varchar(100),
                    posicion_juego varchar(100),
                    nacionalidad varchar(100),
                    equipo varchar(100)
                    )'''
		cur.execute(sql)
		conn.commit()

		return [conn,cur]
	except Exception as e:
		print(e)

	return False

def cargar_jugadores():

	url = "https://www.easports.com/fifa/ultimate-team/api/fut/item?page="
	pagina = 1
	response = requests.get(url+str(pagina))
	datos_fifa = response.json()
	total_paginas = datos_fifa['totalPages']
	[conn,cur] = conectar_BD()

	if conn and cur :

		jugadores = []
		sql = '''INSERT INTO jugador (nombre, posicion_juego, nacionalidad, equipo)	VALUES %s'''

		while(pagina <= total_paginas) :
			datos_jugadores = datos_fifa['items']
			if len(datos_jugadores) > 0:
				jugadores = get_datos_juadores(datos_jugadores)

				try :
					#Insertar por batch 
					extras.execute_values(cur, sql, jugadores)
					conn.commit()
					print("Insertando ",len(jugadores)," jugadores de la página ",pagina,"...")
				except Exception as e:
					print(e)
					print("Error en la página: ",pagina)

				pagina += 1
			else :
				print("No hay datos de jugadores en la página",pagina)

			#import pdb;pdb.set_trace()
			time.sleep(0.1)
			response = requests.get(url+str(pagina))
			datos_fifa = response.json()


	try :
		#Se cierra la comunicación con la base de datos
		conn.close()
		print('Database connection closed.')
		print("\nExtracción finalizada.")
	except Exception as e:
		print("Error al cerrar la conexióna la base de datos")

		
		

