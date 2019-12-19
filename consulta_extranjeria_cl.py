import requests
import json
import threading
import time
import sys

def check_status():
	with open('config.json') as json_data_file:
		data = json.load(json_data_file)

	tiempo_segundos = tiempo_minutos * 60

	threading.Timer(tiempo_segundos, check_status).start()

	payload = {	"names":nombres,
				"surname1":apellido_paterno,
				"surname2":apellido_materno}
	url = data["urls"]["url_action_1"]

	r = requests.get(url, params = payload)

	web = r.text
	
	index = web.find('SeleccionPersona(')
	index2 = web.find(')">') + 1
	web = web[index:index2]
	web = web.replace(" ","")
	web = web.replace("\t","")
	web = web.replace("\n","")
	web = web.replace("\r","")

	web = web[web.find('\'')+1:]

	nodes = []
	counter = 0

	while (counter < 7):
		if (counter > 0):
			web = web[web.find(nodes[counter-1])+len(nodes[counter-1]):]
			web = web[web.find('\',\'')+3:]
		nodes.append(web[:web.find('\'')])
		counter = counter + 1

	try:
		cookie_val = r.cookies['JSESSIONID']
	except:
		print("Ocurrio un error al intentar obtener tu informacion. Intente mas tarde.")
		exit()

	payload2 = {"cod_ext":nodes[0],
				"fec_ext":nodes[1],
				"cod_doc":nodes[2],
				"num_doc":nodes[3],
				"fec_doc":nodes[4],
				"cod_auto":nodes[5],
				"tipo":nodes[6],
				"origen":"Express"}
	url2 = data["urls"]["url_action_2"] + cookie_val

	r2 = requests.Session()
	r2.headers.update({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'})
	r2.headers.update({'Accept-Encoding':'gzip, deflate, br'})
	r2.headers.update({'Accept-Language':'es-ES,es;q=0.9'})
	r2.headers.update({'Cache-Control':'max-age=0'})
	r2.headers.update({'Content-Length':'123'})
	r2.headers.update({'Content-Type':'application/x-www-form-urlencoded'})
	r2.headers.update({'Proxy-Connection':'keep-alive'})
	r2.headers.update({'Upgrade-Insecure-Requests':'1'})
	r2.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})

	r2 = requests.post(url2, data = payload2)

	web = r2.text
	web_before = r2.text

	# we try to find the table that matters
	begin_tag = '<table width="920"'
	end_tag = '</table>'

	# then we trim the string, so we end with just that table
	web = trim_between_tags(web, begin_tag, end_tag)
	
	# next we go for the tbody and again trim the string
	begin_tag = '<tbody>'
	end_tag = '</tbody>'

	web = trim_between_tags(web, begin_tag, end_tag)

	if (nodes[6] == 'PEDE'):
		if (web.find('Permanencia Definitiva otorgada') != -1):
			print('Permanencia Definitiva otorgada')
		elif (web.find('Antecedentes complementarios recibidos') != -1):
			print('Antecedentes complementarios recibidos')
		elif (web.find('Informaci&oacute;n del pago de derechos recibido') != -1):
			print('Información del pago de derechos recibido')
	elif (nodes[6] == 'VISA'):
		if (web.find('Visa de residencia aprobada') != -1):
			print('Visa de residencia aprobada')
		elif (web.find('Visa Estampada') != -1):
			print('	Visa Estampada')
		elif (web.find('Solicitud Aprobada con observaciones') != -1):
			print('	Solicitud Aprobada con observaciones')
		elif (web.find('Solicitud ingresada a an&aacute;lisis con') != -1):
			print('	Solicitud ingresada a análisis con requerimientos previos')
		elif (web.find('Solictud ingresada a an&aacute;lisis sin') != -1):
			print('Solicitud ingresada a análisis sin ningún requerimiento adicional')
	else:
		print(web_before)

	print('')
	print('Tiempo para próxima consulta:')
	countdown(tiempo_segundos)

def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		time_format = '{:02d}:{:02d}'.format(mins,secs)
		print(time_format, end='\r')
		time.sleep(1)
		t -= 1

def trim_between_tags(str, begin_tag, end_tag):
	str = str[str.find(begin_tag):]
	str = str[:str.find(end_tag)+len(end_tag)]
	return str

tiempo_minutos = 30

if __name__ == "__main__" and len(sys.argv) >=5:
	nombres = sys.argv[1] + " " + sys.argv[2]
	apellido_paterno = sys.argv[3]
	apellido_materno = sys.argv[4]

	if len(sys.argv) >= 6:
		time_in_minutes = int(sys.argv[5])
elif __name__ == "__main__":
	name1 = input("Ingresa primer nombre: ")
	name2 = input("Ingresa segundo nombre: ")
	nombres = name1 + " " + name2
	apellido_paterno = input("Ingresa primer apellido: ")
	apellido_materno = input("Ingresa segundo apellido: ")

check_status()