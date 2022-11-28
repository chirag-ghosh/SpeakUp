import io
import requests
import os
import time


def imageToArray(pil_image):
	image_byte_array = io.BytesIO()
	pil_image.save(image_byte_array, format='PNG')
	image_data = image_byte_array.getvalue()
	return image_data


def processRequest( json, data, headers, params ):
	retries = 0
	result = None

	while True:
		response = requests.post('https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/RecognizeText', json = json, data = data, headers = headers, params = params )

		if response.status_code == 429:
			print( "Message: %s" % ( response.json() ) )
			if retries <= int(os.getenv('MaxTrialsPerRequest') or '10'):
				time.sleep(1) 
				retries += 1
				continue
			else: 
				print( 'Error: failed after retrying!' )
				break
		elif response.status_code == 202:
			result = response.headers['Operation-Location']
		else:
			print( "Error code: %d" % ( response.status_code ) )
			print( "Message: %s" % ( response.json() ) )
		break
		
	return result


def getOCRTextResult( operationLocation, headers ):
	retries = 0
	result = None

	while True:
		response = requests.get(operationLocation, json=None, data=None, headers=headers, params=None)
		if response.status_code == 429:
			print("Message: %s" % (response.json()))
			if retries <= int(os.getenv('MaxTrialsPerRequest') or '10'):
				time.sleep(1)
				retries += 1
				continue
			else:
				print('Error: failed after retrying!')
				break
		elif response.status_code == 200:
			result = response.json()
		else:
			print("Error code: %d" % (response.status_code))
			print("Message: %s" % (response.json()))
		break

	return result