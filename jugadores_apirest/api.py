from flask import Flask, jsonify,request
import psycopg2
from config import config
import math
import extraccion_fifa

app = Flask(__name__)



def conectar_BD():
	try :
		#Se extraen los parámetros de configuración de la base de datos
		params = config()
		# Se establece la conexión con la base de datos
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)
		
		# Se crea el cursor
		cur = conn.cursor()
		return [conn,cur]
	except Exception as e:
		print(e)

	return False


def get_paginated_list(results, page, items):
	page = int(page)
	items = int(items)
	count = len(results)
    
	obj = {}
	totalPages = math.ceil(count/items)
	if page < 0 or page > totalPages:
		page = 1
	obj['Page'] = page
	obj['totalPages'] = totalPages
	
	obj['totalItems'] = count
    
	inicio = (page - 1) * items
	fin = (inicio + items)
	
	obj['Players'] = results[inicio:fin]
	obj['Items'] = len(obj['Players'])
	
	return obj

def get_jugadores_x_equipo_bd(equipo,conn,cur):
	sql = '''SELECT nombre,posicion_juego,nacionalidad FROM jugador
			 WHERE UPPER(equipo) like '%{}%' '''.format(equipo)

	print(sql)
	cur.execute(sql)
	jugadores_bd = cur.fetchall()
	
	jugadores = [{'name':jugador[0],
				  'position':jugador[1],
				  'nation':jugador[2]} for jugador in jugadores_bd]
	cur.close()
	conn.close()
	print("PostgreSQL connection is closed")

	return jugadores


@app.route('/')
def inicio():
	return jsonify({'message':'Inicio'})


@app.route('/cargarjugadores')
def cargar_jugadores():
	extraccion_fifa.cargar_jugadores()
	return jsonify({'message':'Jugadores Cargados a la base de datos'})

@app.route('/api/v1/team')
def get_jugadores_x_equipo():

	[conn,cur] = conectar_BD()
	if conn and cur :
		query_parameters = request.args
		equipo = query_parameters.get('name','')
		page = query_parameters.get('page','1')
		jugadores = get_jugadores_x_equipo_bd(equipo.upper(),conn,cur)
		items = 20 #Cantidad de jugadores por página
		if (len(jugadores) > 0):
			return jsonify(get_paginated_list(jugadores,page,items))
	    
		return jsonify({'message': "No se encontraron jugadores del equipo '"+equipo+"'"})
	else:
		return jsonify({'message':'No fue posible conectar con la Base de Datos'})


def get_jugadores_x_nombre_bd(nombre_jugador,orden,conn,cur):
	sql = '''SELECT nombre,posicion_juego,nacionalidad,equipo FROM jugador
			 WHERE UPPER(nombre) like '%{}%' 
			 ORDER BY nombre {}'''.format(nombre_jugador,orden)

	print(sql)
	cur.execute(sql)
	jugadores_bd = cur.fetchall()
	
	jugadores = [{'name':jugador[0],
				  'position':jugador[1],
				  'nation':jugador[2],
				  'team':jugador[3]} for jugador in jugadores_bd]
	cur.close()
	conn.close()
	print("PostgreSQL connection is closed")

	return jugadores


@app.route('/api/v1/players')
def get_jugadores_x_nombre():

	[conn,cur] = conectar_BD()
	if conn and cur :
		query_parameters = request.args

		nombre_jugador = query_parameters.get('search','')
		orden = query_parameters.get('order','ASC')
		page = query_parameters.get('page','1')
		jugadores = get_jugadores_x_nombre_bd(nombre_jugador.upper(),orden.upper(),conn,cur)
		items = 20 #Cantidad de jugadores por página
		if (len(jugadores) > 0):
			return jsonify(get_paginated_list(jugadores,page,items))
	    
		return jsonify({'message': "No se encontraron jugadores con el nombre '"+nombre_jugador+"'"})
	else:
		return jsonify({'message':'No fue posible conectar con la Base de Datos'})


if __name__ == '__main__':
	app.run(debug=True,port=8080,host='0.0.0.0')