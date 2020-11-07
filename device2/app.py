
from flask import Flask, request,render_template
import json
import requests
import ast
import os
from model_train import train
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import cv2

app = Flask(__name__)

cwd = os.getcwd()

@app.route('/')
def hello():
	return render_template('start.html')

@app.route('/sendmodel')
def send_model():
	api_url = 'http://localhost:8000/clientstatus'

	data = {'client_id': '8002'}
	print(data)

	r = requests.post(url=api_url, json=data)
	print(r, r.status_code, r.reason, r.text)
	if r.status_code == 200:
		print("yeah")
		
	file = open(cwd + "/local_model/model2.h5", 'rb')
	data = {'fname':'model2.h5', 'id':'http://localhost:8002/'}
	files = {
		'json': ('json_data', json.dumps(data), 'application/json'),
		'model': ('model2.h5', file, 'application/octet-stream')
	}
	
	req = requests.post(url='http://localhost:8000/cmodel', 
						files=files)
	req1 = requests.post(url='http://localhost:8000/cfile', 
						files=files)
	return render_template("sent.html")

@app.route('/aggmodel', methods=['POST'])
def get_agg_model():
	if os.path.isdir(cwd + '/model_update') == False:
		os.mkdir(cwd + '/model_update')
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		fname = fname['fname']
		print(fname)

		wfile = open(cwd + "/model_update/"+fname, 'wb')
		wfile.write(file)
			
		return "Model received!"
	else:
		return "No file received!"

@app.route('/modeltrain')
def model_train():
	if os.path.isdir(cwd + '/static') == False:
		os.mkdir(cwd + '/static')
	y,z = train()
	accuracy = y["accuracy"]
	loss = y["loss"]
	val_accuracy = y["val_accuracy"]
	val_loss = y["val_loss"]
	N = len(loss) 
	plt.style.use("ggplot")
	plt.figure()
	plt.plot(np.arange(0, N), loss, label="train_loss")
	plt.plot(np.arange(0, N), accuracy, label="train_acc")
	plt.plot(np.arange(0, N), val_loss,label="val_loss" )
	plt.plot(np.arange(0, N), val_accuracy, label="val_acc")
	plt.title("Training Loss and Accuracy for Federated Client 1")
	plt.xlabel("Epochs")
	plt.ylabel("Loss/Accuracy")
	plt.legend(loc="center right")
	plt.savefig(cwd + "/static/plot1.jpg")
	image = [i for i in os.listdir('static') if i.endswith('.jpg')][0]
	
	return render_template('train.html',epoch = len(loss),loss = loss ,accuracy = accuracy,val_loss = val_loss ,val_accuracy = val_accuracy, name = z, user_image = image)


if __name__ == '__main__':
	app.run(host='localhost', port=8002, debug=False, use_reloader=True)
