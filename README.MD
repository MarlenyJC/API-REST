#05-07-2021

##CONTENIDO
fifa21-env : Es el entorno virtual
jugadores_apirest: Contiene la api para cargar y mostrar los jugadores por nombre de jugador o por nombre de equipo
Backend.pdf: Son las instrucciones para realizar la api-rest
Dockerfile : contiene las configuraciones necesarias para levantar el servicio de flask
docker-compose.yml: contiene las imágenes de para el servicio de flask y el de postgresql
req.txt: Los paquetes necesarios para la ejecución de flask con sus funcionalidades


##Descripción
Esta a es una API-REST que permite:
1. Almacenar en una base datos el nombre, pocisión de juego, nacionalidad y equipo de un jugador de futbol
	-La fuente de información es https://www.easports.com/fifa/ultimate-team/api/fut/item?page=1
	desde la página 1 hasta la 908
	-URL: http://localhost:8080/cargarjugadores
	-Parámetros: Sin parámetros
	-El tiempo de duración aproximado para cargar todos los jugadores a la base de datos es de 15-20 minutos

2. Obtiene los jugadores de un equipo sin importar si se escribe en minúscula o mayúscula.
	-URL: http://localhost:8080/api/v1/team
	-Parámetros: 
		*page*: Recibe un número entero (Ej. 1,2,3...), por defualt su valor es 1
		*name*: Recibe una cadena de texto (Ej. juve, juventus, par, paris...)
	-Ejemplo de URL: http://localhost:8080/api/v1/team?name=juve&page=1

3. Busca los jugadores que contengan el String en los campos del nombre del jugador, ya sea una coincidencia parcial o total, y sin importar si 	es mayúscula o minúscula.
	El order puede ser asc o desc y define el orden a partir del nombre alfabéticamente, por default sera asc (si no se recibe en la url).
	-URL: http://localhost:8080/api/v1/players
	-Parámetros:
		*search*: Recibe una cadena de texto (Ej. cristi)
		*order*:  Recibe ASC o DESC, en mayúsculas o minúsculas, puede no enviarse
		*page*:   Recibe un número entero (Ej. 1,2,3...), por defualt su valor es 1
	-Ejemplo de URL: http://localhost:8080/api/v1/players?search=cristi&order=asc&page=1


##Para utilizar el docker-compose
Ubicandose en el directorio donde se cuentra el archivo docker-compose.yml ejecutar:
1. sudo docker-compose build
2. sudo docker-compose up o sudo docker-compose -d
3. Abrir el navegador

##Ejecución de las funcionalidades de la API
*Paso 1.* Ingresar la URL http://localhost:8080 para verificar que el servicio se encuentre activo
*Paso 2.* Cargar los datos de los jugadores a la base de datos http://localhost:8080/cargarjugadores
		-Este proceso requiere de un tiempo aproximado de 15-20 minutos para su ejecución completa
*Paso 3.* Realizar las consultas con cualquiera de las URL de las descripciones *1* y *2* y con un orden indistinto:
		-Ej. http://localhost:8080/api/v1/team?name=juve&page=1
		-Ej. http://localhost:8080/api/v1/players?search=cristi&order=asc&page=1